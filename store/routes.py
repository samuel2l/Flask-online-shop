import smtplib
from flask import render_template, redirect, url_for, flash, request
from store import app
from store.models import Item, Customer, BoughtItems, CartItems
from store.forms import RegisterForm, LoginForm, CartForm, BuyProductForm, SearchForm, RemoveProductForm
from store import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/goods", methods=["GET", "POST"])
@login_required
def goods():
    search_form = SearchForm()
    buy_form = BuyProductForm()
    cart_form = CartForm()

    if request.method == "POST":
        bought_product = request.form.get('bought_product')
        add_to_cart = request.form.get('add_to_cart')

        get_prod_from_db = Item.query.filter_by(name=bought_product).first()
        add_to_cart_table = Item.query.filter_by(name=add_to_cart).first()

        if get_prod_from_db:

            if current_user.amount_in_acc >= get_prod_from_db.price:
                current_user.amount_in_acc -= get_prod_from_db.price
                get_prod_from_db.amnt_in_stock -= 1
                sales_log = BoughtItems(customer_id=current_user.id, item_name=get_prod_from_db.name)
                db.session.add(sales_log)
                db.session.commit()
                flash('Successful Purchase', category='success')
                # #                         msg=f"Subject:Successful Purchase \n\n We recognize your purchase of {get_prod_from_db.name} for {get_prod_from_db.price}, please contact us on +23350389384 to give us your delivery details")
            else:
                flash(
                    f'Account balance not enough. You currently have {current_user.amount_in_acc}$, top up {get_prod_from_db.price - current_user.amount_in_acc}$ to be able to purchase this item',
                    category='danger')

        if add_to_cart_table:
            already_in_cart = CartItems.query.order_by(CartItems.id).all()
            if not already_in_cart:
                cart_log = CartItems(customer_id=current_user.id, item_name=add_to_cart_table.name)
                db.session.add(cart_log)
                db.session.commit()
                flash('Added to your cart')
            else:
                flash('Item already in your cart')
    goodss = Item.query.order_by(Item.name).all()
    return render_template("goods.html", goods=goodss, buy_form=buy_form, cart_form=cart_form, search_form=search_form)


@app.route("/goods/<string:index>")
def goods_info(index):
    for item in Item.query.filter_by(name=index):
        product_name = item.name
        product_info = item.info
        product_price = item.price
        product_img = item.img
        stock_amnt = item.amnt_in_stock

    return render_template("goods_info.html", name=product_name, info=product_info, price=product_price,
                           amnt_in_stock=stock_amnt, img=product_img)


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()

    # if user hits on submit :
    if form.validate_on_submit():
        create_user = Customer(name=form.name.data, email=form.email.data, amount_in_acc=form.amount_in_acc.data,
                               password=form.password.data)
        db.session.add(create_user)
        db.session.commit()
        # log new user in so he can access routes that require log in
        login_user(create_user)
        flash("successful creation", category='success')
        return redirect(url_for('goods'))
    # error handling:
    if form.errors != {}:  # if there are no errors the default dict containing your form errors will be empty obv
        # we will use a for loop to iterate over the erros then use the
        # get_flashed_messages func in the html to display them
        for err in form.errors.values():  # show all the errors as it is possible user has more than one
            flash(f'There was an error: {err}', "danger")

    return render_template('register.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()

    # if user hits on submit :
    if form.validate_on_submit():
        attempted_user = Customer.query.filter_by(email=form.email.data).first()
        # if email exists and the passwords match
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash("successful log in", "success")
            # return f"<div><h1> hey {attempted_user.email}</h1> </div>"
            return redirect(url_for('home'))

        else:
            flash('Username and password do not match', category='danger')
            return redirect(url_for('login_page'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    # ein that
    flash("Successfully logged out", category='info')
    return redirect('/login')


@app.route('/bought')
def bought_items():
    _bought_items = BoughtItems.query.filter_by(customer_id=current_user.id)

    return render_template("bought_goods.html", goods=_bought_items)


@app.route('/cart')
def cart_items():
    _cart_items = CartItems.query.filter_by(customer_id=current_user.id)
    form = RemoveProductForm()
    remove_from_cart = request.form.get('remove_from_cart')

    if form.validate_on_submit():
        remove_from_cart_table = Item.query.filter_by(name=remove_from_cart).first()
        db.session.delete(remove_from_cart_table)
        db.session.commit()
        flash('Remove from your cart')
    return render_template("cart.html", goods=_cart_items,form=remove_from_cart)


@app.route("/filtered", methods=["GET", "POST"])
# def filtered_products():
#     search_form = SearchForm()
#
#     search_product = search_form.name.data
#     # get_prod_from_db = Item.query.filter_by(name=search_product).all()
#     get_prod_from_db = Item.query.filter(Item.name.like(f'%{search_product}%')).all()
#     if not get_prod_from_db:
#         return "<h1>Product you are looking for does not exist </h1>"
#     else:
#         return redirect(url_for('goods_info', index=search_product))


def search():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_product = search_form.name.data
    buy_form = BuyProductForm()
    cart_form = CartForm()

    if request.method == "POST":
        bought_product = request.form.get('bought_product')
        add_to_cart = request.form.get('add_to_cart')

        get_prod_from_db = Item.query.filter_by(name=bought_product).first()
        add_to_cart_table = Item.query.filter_by(name=add_to_cart).first()

        if get_prod_from_db:

            if current_user.amount_in_acc >= get_prod_from_db.price:
                current_user.amount_in_acc -= get_prod_from_db.price
                get_prod_from_db.amnt_in_stock -= 1
                sales_log = BoughtItems(customer_id=current_user.id, item_name=get_prod_from_db.name)
                db.session.add(sales_log)
                db.session.commit()
                flash('Successful Purchase', category='success')
                with smtplib.SMTP("smtp.gmail.com") as connection:

                    connection.starttls()
                    connection.login(user='sama29571@gmail.com', password='ynglmgyiscxlrnmp')
                    connection.sendmail(from_addr='sama29571@gmail.com', to_addrs=current_user.email,
                                        msg=f"Subject:Successful Purchase \n\n We recognize your purchase of {get_prod_from_db.name} for {get_prod_from_db.price}, please contact us on +23350389384 to give us your delivery details")
            else:
                flash(
                    f'Account balance not enough. You currently have {current_user.amount_in_acc}$, top up {get_prod_from_db.price - current_user.amount_in_acc}$ to be able to purchase this item',
                    category='danger')

        if add_to_cart_table:
            already_in_cart = CartItems.query.order_by(CartItems.id).all()
            if not already_in_cart:
                cart_log = CartItems(customer_id=current_user.id, item_name=add_to_cart_table.name)
                db.session.add(cart_log)
                db.session.commit()
                flash('Added to your cart')
            else:
                flash('Item already in your cart')

        # Perform the search with partial match
        get_prod_from_db = Item.query.filter(Item.name.like(f'%{search_product.capitalize()}%')).all()
        if not get_prod_from_db:
            return "<h1>Product you are looking for does not exist</h1>"
        else:
            return render_template('filtered_products.html', items=get_prod_from_db,form=search_form, buy_form=buy_form, cart_form=cart_form)
    return render_template('goods.html', form=search_form, buy_form=buy_form, cart_form=cart_form)
