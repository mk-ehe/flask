from package import app, database
from package.models import Item, User

app.app_context().push()
create = str(input("Chcesz stworzyć nową bazę?(Y/N): ")).lower()

if create == 'y':
    database.create_all()
else: pass

do_what = str(input("Co chcesz dodać?(User / Item / Utwórz relację(rel) / Usuń bazę(del) / Co do kogo należy(nal)): ")).lower()

if do_what == "item":

    name = str(input("Podaj nazwę produktu: "))
    price = int(input("Podaj cenę: "))
    while True:
        barcode = str(input("Podaj kod produktu(12): "))
        if len(barcode) == 12:
            break
        else: pass

    while True:
        description = str(input("Opis(Max:1024): "))
        if len(description) <= 1024:
            break
        else: pass

    item = Item(name = name, price = price, barcode = barcode, description = description)

    database.session.add(item)
    database.session.commit()

    print(Item.query.all())


elif do_what == "usuń bazę" or do_what == "del":
    check = str(input("Napewno?(Y/N): ")).lower()

    if check == "y":
        database.drop_all()
    else: exit(0)
    

elif do_what == "user":

    while True:
        username = str(input("Podaj nazwę użytkownika(Max:30): "))
        if len(username) <= 30:
            break
        else: pass

    while True:
        email = str(input("Podaj adres e-mail(Max:50): "))
        if len(email) <= 50:
            break
        else: pass

    while True:
        password = str(input("Podaj hasło(Max:40): "))
        if len(password) <= 40:
            break
        else: pass
    
    budget = int(input("Podaj swój budżet: "))

    user = User(username = username, email = email, password = password, budget = budget)

    database.session.add(user)
    database.session.commit()

    print(User.query.all())

elif do_what == "rel":
    for item in Item.query.all():
        print(item.name)

    item_to_connect = str(input("Wybierz(wpisz dokładną nazwę): "))
    item_to_connect = Item.query.filter_by(name = item_to_connect).first()

    for user in User.query.all():
        print(user.username)

    who = str(input("Do kogo chcesz przypisać(wpisz dokładnią nazwę): "))

    item_to_connect.owner = User.query.filter_by(username = who).first().id

    database.session.add(item_to_connect)
    database.session.commit()


elif do_what == "nal" or do_what == "co do kogo należy":
    for item in Item.query.all():
        print(item.name)

    what_itm = str(input("Wpisz dokładną nazwę: "))
    what_itm = Item.query.filter_by(name = what_itm).first()
    print(what_itm.owned_by)


else: exit(0)

if do_what != "nal" and do_what != "co do kogo należy":
    while True:
        roll_b = str(input("Czy chcesz cofnąć zmiany?(Y/N): ")).lower()
        if roll_b == 'n':
            exit(0)

        elif roll_b == 'y':
            database.session.rollback()
            exit(0)

        else: pass