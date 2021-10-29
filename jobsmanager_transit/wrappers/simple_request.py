class SimpleRequest:
    def __init__(self, data, remote_ip):
        self.arguments = data
        self.body_arguments = data
        self.remote_ip = remote_ip
