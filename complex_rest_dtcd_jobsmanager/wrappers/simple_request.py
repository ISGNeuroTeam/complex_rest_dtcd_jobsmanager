class SimpleRequest:

    @staticmethod
    def _convert_to_bin_and_put_in_list(data):
        for k in data.keys():
            data[k] = [data[k].encode('utf-8')]

    @staticmethod
    def _get_client_ip(request_meta):
        x_forwarded_for = request_meta.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request_meta.get('REMOTE_ADDR')
        return ip

    def __int__(self, request):
        data = request.data.copy()
        self._convert_to_bin_and_put_in_list(data)
        self.arguments = data
        self.body_arguments = data
        self.remote_ip = self._get_client_ip(request.META)

    def __init__(self, data, remote_ip):
        self._convert_to_bin_and_put_in_list(data)
        self.arguments = data
        self.body_arguments = data
        self.remote_ip = remote_ip
