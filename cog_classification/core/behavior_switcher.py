class BehaviorSwitcher:
    """
    This class implements behavior changing in time.

    :param behaviors: dictionary with time of change (hashable) as a key and behavior as a value, \
                      or one behavior that will be manifested from the start (1. iteration).
    :type behaviors: dictionary or single behavior.

    :raise: **ValueError** - if behaviors is None.

    If more than one behavior was passed then behavior switcher will be replacing old behavior with newer one,
    when newer behavior time of change will be passed by change method.
    \ To initialize current behavior change method should be used.
    \ If you want to use update method of BehaviorSwitcher time of change should be numeric.
    """

    def __init__(self, behaviors):
        if behaviors is not None:
            if isinstance(behaviors, dict):
                self.behaviors = behaviors
            else:
                self.behaviors = {1L: behaviors}
        else:
            raise ValueError
        self.current_behavior = None

    def change(self, change_time):
        """
        Changes current behavior on behavior associated with change time.

        :param hashable change_time: the current time that can cause behavior changing.

        If there is no new behavior associated with time of change, method leaves the old value of current behavior.
        """

        if change_time in self.behaviors:
            self.current_behavior = self.behaviors[change_time]

    def update(self, changing_class, time):
        """
        Adds behaviors moved by time from changing class to self.

        :param BehaviorSwitcher changing_class: instance whose content is added to self.
        :param long time: how much should be behaviors form changing class moved forward.

        :raise: **TypeError** - if basic time change is not numeric.
        """
        for change, behavior in changing_class.behaviors.iteritems():
            self.behaviors[change + time] = behavior
