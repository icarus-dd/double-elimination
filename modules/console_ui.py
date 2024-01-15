class UI:

    @staticmethod
    def emit(msg):
        print(msg)

    def query(self, msg, add_linebreak=False, options=None):
        __msg = msg
        if options:
            __msg += " ("
            __msg += '/'.join(options.upper())
            __msg += ") "

        if add_linebreak:
            __msg += "\n"

        result = input(__msg)
        if options:
            result = result.upper()

        if options and not result[0].upper() in options.upper():
            return self.query(msg, add_linebreak, options)

        return result
