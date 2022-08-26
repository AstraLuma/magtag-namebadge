BUFFSIZE = 64

class FingerServ:
    def user_info(self, send, username, verbose):
        raise NotImplementedError

    def list_users(self, send, verbose):
        raise NotImplementedError

    def __call__(self, conn):
        try:
            recvbuff = bytearray(BUFFSIZE)
            linebuff = bytearray()

            while '\n' not in linebuff:
                try:
                    cnt = conn.recv_into(recvbuff, len(recvbuff))
                except OSError as exc:
                    if exc.errno == 11:  # EAGAIN
                        continue
                    else:
                        raise
                else:
                    linebuff += recvbuff[:cnt]

                    if not cnt:
                        break

                    if len(linebuff) > BUFFSIZE * 8:
                        # Too long
                        conn.send(b"no. request too long.\n")
                        return

            if b'@' in linebuff:
                # not implemented
                conn.send(b"no. go ask them yourself.\n")
                return

            line = linebuff.decode('utf-8')
            print("received", repr(line))

            del linebuff, recvbuff

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