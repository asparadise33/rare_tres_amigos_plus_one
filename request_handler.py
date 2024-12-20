from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
import json



from views import create_user, login_user, get_all_users, update_user, get_single_user, delete_user, get_all_comments, get_single_comment, create_comment, update_comment, delete_comment, get_all_posts, get_single_post, create_post, get_all_subscriptions, get_single_subscription, delete_post, create_subscription, update_subscription, update_post, delete_subscription





class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = self.path.split('/')
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        """Handle Get requests to the server"""
        self._set_headers(200)
        response = {}
        parsed = self.parse_url(self.path)

        if '?' not in self.path:
            ( resource, id ) = parsed

            if resource == "users":
                if id is not None:
                    response = get_single_user(id)

                else:  
                    response = get_all_users()
                    
            
            if resource == "comments":
                if id is not None:
                    response = get_single_comment(id)

                else:  
                    response = get_all_comments()
                    
            if resource == "posts":
                if id is not None:
                    response = get_single_post(id)

                else:
                    response = get_all_posts()
            
            if resource == "subscriptions":
                if id is not None:
                    response = get_single_subscription(id)

                else:
                    response = get_all_subscriptions()           
       
        self.wfile.write(json.dumps(response).encode())


    def do_POST(self):
        """Make a post request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len))
        response = ''
        resource, _ = self.parse_url(self.path)

        if resource == 'login':
            response = login_user(post_body)
        if resource == 'register':
            response = create_user(post_body)
        if resource == 'users':
            response = create_user(post_body)
        if resource == 'posts':
            resource = create_post(post_body)
        if resource == 'subscriptions':
            resource = create_subscription(post_body)
        if resource == 'comments':
            resource = create_comment(post_body)
            
        self.wfile.write(json.dumps(response).encode())

    def do_PUT(self):
        """Handles PUT requests to the server"""
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "users":
           success = update_user(id, post_body)

        if resource == "posts":
            success = update_post(id, post_body)
            
        if resource == "comments":
            success = update_comment(id, post_body)    
            
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)
            
        if resource == "subscriptions":
           success = update_subscription(id, post_body)
    
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)
            
        if resource == "subscriptions":
           success = update_subscription(id, post_body)
    
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        """Handle DELETE Requests"""
        self._set_headers(204)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)

        if resource == "posts":
          delete_post(id)

        if resource == "users":
          delete_user(id)  
        
        if resource == "subscriptions":
          delete_subscription(id)  
          
        if resource == "comments":
          delete_comment(id) 
          
        self.wfile.write("".encode())


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
