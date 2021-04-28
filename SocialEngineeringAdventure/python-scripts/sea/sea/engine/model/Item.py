class Item:
    def __init__(self, name, effect="", is_consumable=False, value=0, passage_name="", qta=0):
        self.name = name
        self.effect = effect
        self.is_consumable = is_consumable
        self.qta = qta
        self.passage_name = passage_name
        self.value = value

    def set_qta(self, qta):
        self.qta = qta

    def add(self, qta):
        self.qta += qta

    def use(self):
        self.qta -= 1
        return self.qta > 0

    def qta_visible(self):
        return self.is_consumable

    def __str__(self):
        if self.is_consumable:
            return "{} {} {} qta={}".format(self.name, self.descr, self.effect, self.qta)
        else:
            return "{} {} {}".format(self.name, self.descr, self.effect)
