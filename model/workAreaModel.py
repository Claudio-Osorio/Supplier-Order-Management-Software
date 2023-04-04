class workAreaModel:
    def __init__(self):


        # Returns tuples of selected children
        def GetCurrSelected(self):
            selection = self.order_tree.selection()
            list_selected = list()
            for index in selection:
                value = self.order_tree.item(index, 'values')
                list_selected.append(value)
            return list_selected

        # Returns tuples of all children
        def GetAllCurrChildren(self):
            all_children = self.order_tree.get_children()
            list_all = list()
            for index in all_children:
                value = self.order_tree.item(index, 'values')
                list_all.append(value)
            return list_all
