def set_products_bpth (self):  # , bpt):
  # return self.title_or_id() # returns the containing folder - good.
  # return self.products.title_or_id() # works - good

  # so now, set the hook to go here, to *this* folder's (out-of-band) bpth method.
  self.products.__before_publishing_traverse__ = self.bpth
  return 'OK'


def set_faq_bpth (self):
  self.faq.__before_publishing_traverse__ = self.bpth_faq
  return 'OK - faq bpth set!'


def set_quiet_bpth (self):
  self.quiet.__before_publishing_traverse__ = self.bpth_quiet
  return 'OK - quiet bpth set!'


def reset_bpths (self):  # not tested!
  del self.faq.__before_publishing_traverse__
  del self.products.__before_publishing_traverse__ 
  del self.quiet.__before_publishing_traverse__ 
  return 'OK - all bpths reset!'