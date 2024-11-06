from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models.subscriptions import Subscription
from ..models.subscriptions import Wallet
from ..forms import SubscriptionForm
from ..database import db
from datetime import datetime
from ..forms  import WalletRechargeForm

subscriptions_bp = Blueprint('subscriptions', __name__)

@subscriptions_bp.route('/subscribe', methods=['GET', 'POST'])
@login_required
def subscribe():
    form = SubscriptionForm()
    wallet = current_user.wallet
    
    if form.validate_on_submit():
        if wallet and wallet.balance >= form.cost.data:
            wallet.balance -= form.cost.data
            wallet.last_used = datetime.utcnow()
            
            subscription = Subscription(
                user_id=current_user.user_id,
                plan_name=form.plan_name.data,
                start_date=datetime.utcnow(),
                status='active'
            )
            db.session.add(subscription)
            db.session.commit()
            flash('Subscription purchased successfully!', 'success')
            return redirect(url_for('subscriptions.subscribe'))
        else:
            flash('Insufficient wallet balance. Please recharge.', 'danger')

    return render_template('subscribe.html', form=form, wallet=wallet)



@subscriptions_bp.route('/recharge', methods=['GET', 'POST'])
@login_required
def recharge():
    form = WalletRechargeForm()
    
    if form.validate_on_submit():
        if not current_user.wallet:
            wallet = Wallet(user_id=current_user.user_id, balance=form.amount.data, last_recharge=datetime.utcnow())
            db.session.add(wallet)
        else:
            current_user.wallet.balance += form.amount.data
            current_user.wallet.last_recharge = datetime.utcnow()

        db.session.commit()
        flash('Wallet recharged successfully!', 'success')
        return redirect(url_for('subscriptions.recharge'))

    return render_template('recharge_wallet.html', form=form)
