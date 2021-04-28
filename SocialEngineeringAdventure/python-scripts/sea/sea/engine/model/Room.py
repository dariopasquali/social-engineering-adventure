class Room:

    def __init__(self, name, start_passage, right_passage, left_passage="", back_passage="", backtrack_passage=""):
        self.name = name
        self.back_passage = back_passage
        self.start_passage = start_passage
        self.right_passage = right_passage
        self.left_passage = left_passage

        self.backtrack_passage = backtrack_passage

        self.passages = {}
        self.links = {}

    def get_start_passage(self):
        return self.passages[self.start_passage]

    def get_right_choice(self):
        return self.passages[self.right_passage]

    def get_left_choice(self):
        if self.left_passage != "":
            return self.passages[self.left_passage]
        return None

    def get_back_choice(self):
        if self.back_passage != "":
            return self.passages[self.back_passage]
        return None

    def get_backtrack_passage(self):
        if self.backtrack_passage != "":
            return self.passages[self.backtrack_passage]
        return None

    def get_passage(self, passage):
        return self.passages[passage]

    def get_links(self, from_p):
        return self.links[from_p]

    def is_crossroad(self):
        return self.right_passage != "" and self.left_passage != ""

    def allow_backtrack(self):
        return self.back_passage != ""

    def __count_endpoints(self):
        cnt = 0
        if self.right_passage != "":
            cnt += 1
        if self.left_passage != "":
            cnt += 1
        if self.back_passage != "":
            cnt += 1

        return cnt

    def add_passage(self, passage):
        self.passages[passage.name] = passage

    def add_links(self, passage, links):
        self.links[passage] = links

    def __str__(self):
        ret_str = "===== ROOM =====\n"
        ret_str += "name: {}\n".format(self.name)
        ret_str += "outcomes: {}\n".format(self.__count_endpoints())
        ret_str += "start passage: {}\n".format(self.start_passage)
        ret_str += "end passage right: {}\n".format(self.right_passage)
        ret_str += "end passage left: {}\n".format(self.left_passage)
        return ret_str

    def to_json(self):

        json_dict = {'name': self.name,
                     'start': self.start_passage,
                     'outcomes': self.__count_endpoints(),
                     'allow_backtrack': self.back_passage != "",
                     'passages': {},
                     'links': {}
                     }
        for name, passage in self.passages.items():
            json_dict['passages'][name] = passage.to_json()

        for from_p, to_ps in self.links.items():
            json_dict['links'][from_p] = {'source': from_p, 'destinations': to_ps}

        return json_dict
