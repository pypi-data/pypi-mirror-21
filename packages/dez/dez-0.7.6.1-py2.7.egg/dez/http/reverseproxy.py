from dez.network import SocketDaemon, SimpleClient
from datetime import datetime

class ReverseProxyConnection(object):
    def __init__(self, conn, h1, p1, h2, p2, logger, start_data):
        self.front_conn = conn
        self.front_host = h1
        self.front_port = p1
        self.back_host = h2
        self.back_port = p2
        self.logger = logger
        self.log("Initializing connection")
        SimpleClient().connect(h2, p2, self.onConnect, [start_data])

    def log(self, msg):
        self.logger("%s:%s -> %s:%s > %s"%(self.front_host, self.front_port, self.back_host, self.back_port, msg))

    def onConnect(self, conn, start_data):
        self.log("Connection established")
        self.back_conn = conn
        self.front_conn.set_close_cb(self.onClose, [self.back_conn])
        self.back_conn.set_close_cb(self.onClose, [self.front_conn])
        self.front_conn.set_rmode_close_chunked(self.back_conn.write)
        self.back_conn.set_rmode_close_chunked(self.front_conn.write)
        self.back_conn.write(start_data)

    def onClose(self, conn):
        self.log("Connection closed")
        self.front_conn.set_close_cb(None)
        self.back_conn.set_close_cb(None)
        self.front_conn.halt_read()
        self.back_conn.halt_read()
        self.front_conn = None
        self.back_conn = None
        conn.soft_close()

BIG_302 = True
BIG_FILES = ["mp3", "png", "jpg", "jpeg", "gif", "pdf", "csv", "mov",
    "zip", "doc", "docx", "jar", "data", "db", "xlsx", "geojson"] # more?

class ReverseProxy(object):
    def __init__(self, port, verbose, redirect=False, protocol="http", certfile=None):
        self.port = port
        self.default_address = None
        self.verbose = verbose
        self.redirect = redirect
        self.protocol = protocol
        self.domains = {}
        self.daemon = SocketDaemon('', port, self.new_connection, certfile=certfile)

    def log(self, data):
        if self.verbose:
            print "[%s] %s"%(datetime.now(), data)

    def new_connection(self, conn):
        conn.set_rmode_delimiter('\r\n\r\n', self.route_connection, [conn])

    def _302(self, conn, domain, path): # from hostTrick
        conn.write("HTTP/1.1 302 Found\r\nLocation: %s://%s%s\r\n\r\n"%(self.protocol, domain, path))
        conn.soft_close()

    def domain2hostport(self, domain):
        if domain in self.domains:
            return self.domains[domain]
        if self.default_address:
            return self.default_address
        return None, None

    def cantroute(self, domain, conn):
        msg = "unable to route hostname: %s"%(domain,)
        self.log(msg)
        conn.close(msg)

    def route_connection(self, data, conn):
        conn.halt_read()
        domain = None
        path = None
        should302 = self.redirect
        for line in data.split('\r\n'):
            if line.startswith("GET"):
                path = line.split(" ")[1]
                if "." in path and path.rsplit(".")[1] in BIG_FILES:
                    should302 = True
            elif line.startswith('Host: '):
                domain = line[6:]
                if ":" in domain:
                    domain = domain.split(":")[0]
                break
        if not domain:
            return conn.close('no host header')
        self.dispatch(data+'\r\n\r\n', conn, domain, should302, path)

    def dispatch(self, data, conn, domain, should302=False, path=None):
        host, port = self.domain2hostport(domain)
        if not host:
            return self.cantroute(domain, conn)
        if should302 and BIG_302:
            self._302(conn, "%s:%s"%(host, port), path)
        else:
            ReverseProxyConnection(conn, domain, self.port, host, port, self.log, data)

    def register_default(self, host, port):
        self.default_address = (host, port)

    def register_domain(self, domain, host, port):
        self.domains[domain] = (host, port)

    def start(self):
        self.daemon.start()

def error(msg):
    print "error:",msg
    import sys
    sys.exit(0)

def startreverseproxy():
    global BIG_302
    import os, optparse
    parser = optparse.OptionParser('dez_reverse_proxy [CONFIG]')
    parser.add_option("-v", "--verbose", action="store_true",
        dest="verbose", default=False, help="log proxy activity")
    parser.add_option("-p", "--port", dest="port", default="80",
        help="public-facing port (default: 80)")
    parser.add_option("-o", "--override_redirect", action="store_true",
        dest="override_redirect", default=False,
        help="prevent 302 redirect of large files (necessary if incoming host matters to target)")
    parser.add_option("-c", "--cert", dest="cert", default=None,
        help="your ssl certificate -- if port is unspecified, uses port 443")
    parser.add_option("-s", "--ssl_redirect", dest="ssl_redirect", default=None,
        help="if specified, 302 redirect ALL requests to https (port 443) application at specified host - ignores config")
    options, arguments = parser.parse_args()
    BIG_302 = not options.override_redirect
    if options.cert and options.port == "80":
        options.port = 443
    else:
        try:
            options.port = int(options.port)
        except:
            error('invalid port specified -- int required')
    try:
        controller = ReverseProxy(options.port, options.verbose, certfile=options.cert)
    except Exception, e:
        error(options.verbose and "failed: %s"%(e,) or 'could not start server! try running as root!')
    if options.ssl_redirect:
        controller.redirect = True
        controller.protocol = "https"
        print "Redirecting traffic to https (port 443)"
        controller.register_default(options.ssl_redirect, 443)
    else:
        if len(arguments) < 1:
            error("no config specified")
        config = arguments[0]
        if not os.path.isfile(config):
            error('no valid config - "%s" not found'%config)
        f = open(config)
        lines = f.readlines()
        f.close()
        for line in lines:
            line = line.split("#")[0]
            if line: # allows comment lines
                try:
                    domain, back_addr = line.split('->')
                    domain = domain.strip()
                    host, port = back_addr.split(':')
                    host = host.strip()
                    port = int(port)
                except:
                    error('could not parse config. expected "incoming_hostname -> forwarding_address_hostname:forwarding_address_port". failed on line: "%s"'%line)
                if domain == "*":
                    print "Setting default forwarding address to %s:%s"%(host, port)
                    controller.register_default(host, port)
                else:
                    print "Mapping %s to %s:%s"%(domain, host, port)
                    controller.register_domain(domain, host, port)
    print "Starting reverse proxy router on port %s"%(options.port)
    controller.start()
