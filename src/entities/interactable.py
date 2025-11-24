class Interactable:
    def __init__(self, char_id):
        self.id = char_id
        # self.image = load_image(f"characters/{char_id}.png")
        self.dialog_text = f"Hello, I am {char_id}"
        self.dialog_options = ["Option 1", "Option 2", "Option 3"]
