import main

print('App routes:')
for route in main.app.routes:
    print(route.path)