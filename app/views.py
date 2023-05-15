from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView
from .models import Item, OrderItem, Order, Payment, ContactModel
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import CustomUser
import stripe
from django.conf import settings
from . import forms
from .forms import SearchForm, ContactForm
from django.views.generic.edit import FormView

class ShopView(View):
    def get(self, request, *args, **kwargs):
        item_data =  Item.objects.all()
        form = forms.ContactForm()
        context = {
            'item_data': item_data,
            'form': form,
        }
        return render(request, 'app/shop.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST or None)
        context = {
            "form": form,
        }

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            obj = ContactModel(name=name, email=email, subject=subject, message=message)
            obj.save()

        return render(request, 'app/form-thanks.html', context)

class DiagnoseView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/diagnose.html')

class IntroduceView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/introduce.html')

class FundamentalView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/fundamental.html')

class CommentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/comment.html')

class IndexView(ListView):
    def get(self, request, *args, **kwargs):
        item_data =  Item.objects.all()
        searchForm = SearchForm(request.GET or None)
        context = {
            'item_data': item_data,
            'searchForm': SearchForm,
        }
            
        if searchForm.is_valid():
            keyword = searchForm.cleaned_data['keyword']
            context["item_data"] = Item.objects.filter(description__contains=keyword)
        else:
            searchForm = SearchForm()
            item_data = Item.objects.all()
        
        return render(request, 'app/index.html', context)

class IndexListView(IndexView):

    # 引数でを受け取ったkeyでItemモデルにフィルターをかけて表示
    def get(self, request, key, *args, **kwargs):
        keyword = key
        context = {
            'item_data': Item.objects.filter(description__contains=keyword),
            'searchForm': SearchForm,
        }

        return render(request, 'app/index.html', context)

class ItemDetailView(View):
     def get(self, request, *args, **kwargs):
        item_data = Item.objects.get(slug=self.kwargs['slug'])
        context =  {
            'item_data': item_data,
        }
        return render(request, 'app/product.html', context)

@login_required
def addItem(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order = Order.objects.filter(user=request.user, ordered=False)

    if order.exists():
        order = order[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        order = Order.objects.create(user=request.user, ordered_date=timezone.now())
        order.items.add(order_item)

    return redirect('/order/')

class OrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            context = {
                'order': order
            }
            return render(request, 'app/order.html', context)
        except ObjectDoesNotExist:
            return render(request, 'app/order.html')

class ContactFormView(FormView):
    def post(self, request, *args, **kwargs):
        obj = ContactModel.objects.get()
        form = ContactForm(request.POST or None)
        
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            obj.name = name
            obj.email = email
            obj.subject = subject
            obj.message = message
            obj.save()
            return render(request, 'app/form-thanks.html')

        return render(request, 'app/form-thanks.html')

@login_required
def removeItem(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order = Order.objects.filter(
        user=request.user, 
        ordered=False
    )
    if order.exists():
        order = order[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            return redirect('/order/')

    return redirect('product', slug=slug)

@login_required
def removeSingleItem(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order.exists():
        order = order[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.delete()
            return redirect('/order/')

    return redirect('product', slug=slug)

class PaymentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(user=request.user, ordered=False)
        user_data = CustomUser.objects.get(id=request.user.id)
        context = {
            'order': order,
            'user_data': user_data
        }
        return render(request, 'app/payment.html', context)

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        order = Order.objects.get(user=request.user, ordered=False)
        token = request.POST.get('stripeToken')
        order_items = order.items.all()
        amount = order.get_total()
        item_list = []
        for order_item in order_items:
            item_list.append(str(order_item.item) + ':' + str(order_item.quantity))
        description = ' '.join(item_list)

        charge = stripe.Charge.create(
            amount=amount,
            currency='jpy',
            description=description,
            source=token
        )

        payment = Payment(user=request.user)
        payment.stripe_change_id = charge['id']
        payment.amount = amount
        payment.save()

        order_items.update(ordered=True)
        for item in order_items:
            item.save()

        order.ordered = True
        order.payment = payment
        order.save()
        return redirect('thanks')

class ThanksView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/thanks.html')

