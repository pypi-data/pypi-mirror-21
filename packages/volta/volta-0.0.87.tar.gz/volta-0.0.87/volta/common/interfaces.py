class VoltaBox(object):
    """ Volta box interface
    Parent class for volta boxes
    """
    def __init__(self, config):
        """ parse config stage """
        pass

    def start_test(self, results):
        """ Grab stage
        Args:
            `results` - should be an object, answers to .put() and .get(), e.g. queue.Queue()
        """
        raise NotImplementedError("Abstract method needs to be overridden")

    def end_test(self):
        """ end test """
        raise NotImplementedError("Abstract method needs to be overridden")

    def add_sink(self, queue):
        """ add listener """
        raise NotImplementedError("Abstract method needs to be overridden")


class Phone(object):
    """ Phone interface
    Parent class for phones
    """
    def __init__(self, config, volta):
        """ parse config stage """
        pass

    def prepare(self):
        """ install apps, unplug device """
        raise NotImplementedError("Abstract method needs to be overridden")

    def start(self):
        """ make sync w/ flashlight """
        raise NotImplementedError("Abstract method needs to be overridden")

    def run_test(self):
        """ run app """
        raise NotImplementedError("Abstract method needs to be overridden")

    def end(self):
        """ stop volta, plug device and get logs """
        raise NotImplementedError("Abstract method needs to be overridden")