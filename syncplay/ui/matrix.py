from matrix_client.client import MatrixClient
from threading import Thread


class Matrix(Thread):
    
    def __init__(self, ui, url, token, user_id, room_id):
        Thread.__init__(self)
        self.ui = ui
        self.client = MatrixClient(url, token=token, user_id=user_id)
        self.room_id = room_id
        self.user_id = user_id
        self.client.add_listener(self.incoming_message)
        self.running = True
        self.start()

    def run(self):
        try:
            while(self.running):
                self.client.listen_for_events(10000)
        except Exception as e:
            print("Error connecting to Matrix:", e)
            
    def incoming_message(self, chunk):
        if (chunk["type"] == "m.room.message" and chunk["room_id"] == self.room_id and chunk["sender"] == self.user_id and 
        chunk["content"]["body"][:1] != '<'):
            self.ui.chatInput.setText(chunk["content"]["body"])
            self.ui.chatButton.click()

    def send_message(self, text):
        if text[:1] == "<":
            self.client.rooms[self.room_id].send_text(text)

    def stop(self):
        self.running = False
        self.join()
