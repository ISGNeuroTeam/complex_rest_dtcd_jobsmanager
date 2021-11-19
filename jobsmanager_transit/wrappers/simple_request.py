class SimpleRequest:
    def __init__(self, data, remote_ip):
        self.convert_to_bin_and_put_in_list(data)
        self.arguments = data
        self.body_arguments = data
        self.remote_ip = remote_ip

    @staticmethod
    def convert_to_bin_and_put_in_list(data):
        for k in data.keys():
            data[k] = [data[k].encode('utf-8')]
