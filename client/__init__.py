import asyncio

import socketio

sio = socketio.AsyncClient()
loop = asyncio.get_event_loop()


async def main():
    print("Connect")
    await sio.connect("http://localhost:5000")
    await sio.wait()


@sio.event
async def connect():
    name = input("Your name: ")
    icon = input("Your icon: ")

    def callback(data):
        print(data)
        errors = data["errors"]
        if len(errors) > 0:
            error = errors[0]
            print(f"Error {error} occured")
            exit(1)

    await sio.emit("register_user", {"name": name, "icon": icon}, callback=callback)


@sio.event
async def message(data):
    print(data["message"])


@sio.event
async def set_field_location():
    return int(input("Field Location: "))


if __name__ == "__main__":
    loop.run_until_complete(main())
