BUFFSIZE = 512

recvbuff = bytearray(BUFFSIZE)

class FingerServ:
    def user_info(self, send, username, verbose):
        raise NotImplementedError

    def list_users(self, send, verbose):
        raise NotImplementedError

    def __call__(self, conn):
        try:
            cnt = conn.recv_into(recvbuff, len(recvbuff))

            if cnt == len(recvbuff):
                # Too long
                conn.send(b"no. request too long.\n")
                return

            if b'@' in recvbuff:
                # not implemented
                conn.send(b"no. go ask them yourself.\n")
                return

            line = recvbuff[:cnt].decode('utf-8')
            print("received", repr(line))

            # Parse it out
            if line.startswith('/W '):
                line = line[3:]
                verbose = True
            else:
                verbose = False

            name = line.strip()

            print(f"finger {name} ({verbose=})")

            send = lambda txt: conn.send(txt.encode('utf-8'))
            if name:
                # Info on user
                self.user_info(send, name, verbose=True)
            else:
                # List users
                self.list_users(send, verbose=True)
        finally:
            conn.close()