from jarkom import init, serve

if __name__ == '__main__':
    server = init()
    print(f'Serving on http://{server["addr"][0]}:{server["addr"][1]}')
    serve(server)
