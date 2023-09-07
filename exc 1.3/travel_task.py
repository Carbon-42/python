destination = input('Where would you like to travel to? ')
destination = destination.upper()

if destination == 'PRINCE EDWARD ISLAND' \
        or destination == 'NEW YORK' \
        or destination == 'COLUMBIA':
    print('Enjoy your stay in', destination + '!')
else:
    print('Sorry that destination is not available at this time.')
