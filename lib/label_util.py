

from OCC.TDF import TDF_ChildIterator


def tag_list(label):
    """Return the full list of tags for a label (e.g. [0, 0, 1, 2])"""
    # the functionality of this duplicates that of TDF_Tool.TagList in a
    # more pythonic way
    list = []
    while True:
        list.insert(0, label.Tag())
        if label.IsRoot():
            return list
        label = label.Father()


def child_list(label):
    """Return a list of all child labels of the given label"""
    list = [tag_list(label)]
    ci = TDF_ChildIterator()
    ci.Initialize(label)
    while ci.More():
        list.append(tag_list(ci.Value()))
        ci.Next()
    return list
