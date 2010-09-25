#!/usr/bin/python

class UploaderIface:
    """ Uploader interface
    """

    def __init__(self, host, distribution, changes):
        """ Constructor
        :param host the hostname of the destination
        :param distribution the target distribution this upload applies to
        :param changes the changes filename
        """
        pass

    def upload(self):
        """ Starts the upload process
        """
        self.pre_upload()
        retval = False
        if self.do_upload() == False:
            self.post_failed_upload()
        else:
            self.post_successful_upload()
            retval = True
        self.post_upload()
        return retval

    #protected
    def pre_upload(self):
        """ Does preparation before starting the upload
        """
        pass

    def post_successful_upload(self):
        """ Does cleaning up after a successful upload
        """
        pass

    def post_failed_upload(self):
        """ Does cleaning up after a failed upload
        """
        pass

    def post_upload(self):
        """ Does further cleaning after an upload
        """
        pass

    def do_upload(self):
        """ Does the uploading
        """
        pass
