from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

import helpers
from api.models import Transaction, User, Wallet
from api.serializers import UserSerializer, WalletSerializer, TransactionSerializer
from permissions import ActionBasedPermission, IsAdmin, IsElite


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        AllowAny: ['create'],
        IsAuthenticated: ['retrieve', 'list'],
    }

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            if data.get('user_type') != "admin":
                Wallet.objects.create(owner=user, currency=data['currency'], main_wallet=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'], permission_classes=[IsAdmin])
    def change_user_type(self, request):
        try:
            user_id = request.data.get('user_id')
            user_type = request.data.get('user_type')
            user = User.objects.get(id=user_id)
            if user.user_type not in ["noob", "elite"]:
                return Response({"message": "Uer is neither a noob nor an elite"}, status=status.HTTP_400_BAD_REQUEST)
            user.user_type = user_type
            user.save()
            return Response({"message": "Action performed successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "This user does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class WalletViewSet(viewsets.ViewSet):
    queryset = Wallet.objects.all()

    @action(detail=False, methods=['post'], permission_classes=[IsElite])
    def create_wallet(self, request):
        data = request.data
        try:
            token = Token.objects.get(key=request.auth.key)
            data.update({'owner': token.user.pk})
            serializer = WalletSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def view_wallets(self, request):
        try:
            token = Token.objects.get(key=request.auth.key)
            wallets = Wallet.objects.filter(owner=token.user)
            serializer = WalletSerializer(wallets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def fund_wallet(self, request):
        data = request.data
        amount = data.get('amount', 0)
        currency = data.get('currency')
        wallet_id = data.get('wallet_id')
        try:
            token = Token.objects.get(key=request.auth.key)
            user_type = token.user.user_type
            if user_type != "admin":
                if user_type == 'noob':
                    wallet = Wallet.objects.get(owner=token.user)
                    amount_conversion = helpers.convert_to_main_currency(amount, currency, wallet)
                    Transaction.objects.create(
                        wallet=wallet, amount=amount_conversion, transaction_type='funding'
                    )
                else:
                    wallet = Wallet.objects.get(currency=currency, owner=token.user)
                    wallet.balance = wallet.balance + amount
                    wallet.save()
                    return Response({"message": "Wallet funded successfully"}, status=status.HTTP_200_OK)
            else:
                wallet = Wallet.objects.get(currency=currency, id=wallet_id)
                helpers.perform_funding(amount, wallet)
                return Response({"message": "Wallet funded successfully"}, status=status.HTTP_200_OK)
            return Response({"message": "Wallet will be funded as soon as an admin approves."},
                            status=status.HTTP_200_OK)
        except Wallet.DoesNotExist:
            return Response({"message": "This wallet does not exist or is not yours"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def withdraw(self, request):
        data = request.data
        amount = data.get('amount', 0)
        currency = data.get('currency')
        wallet_id = data.get('wallet_id')
        try:
            token = Token.objects.get(key=request.auth.key)
            user_type = token.user.user_type
            if user_type != 'admin':
                wallet = Wallet.objects.get(owner=token.user, id=wallet_id)
                if user_type == "noob":
                    amount_conversion = helpers.convert_to_main_currency(amount, currency, wallet)
                    if wallet.balance < amount_conversion:
                        return Response({"message": "Balance below withdraw-able amount."},
                                        status=status.HTTP_400_BAD_REQUEST)
                    else:
                        Transaction.objects.create(
                            wallet=wallet, amount=amount_conversion, transaction_type='withdrawal'
                        )
                elif wallet.balance >= amount:
                    Transaction.objects.create(wallet=wallet, amount=amount, transaction_type='withdrawal')
                else:
                    amount_conversion = helpers.convert_to_main_currency(amount, currency, wallet)
                    main_wallet = Wallet.objects.get(owner=token.user, main_wallet=True)
                    if main_wallet.balance < amount_conversion:
                        return Response({"message": "Balance below withdraw-able amount."},
                                        status=status.HTTP_400_BAD_REQUEST)
                    else:
                        Transaction.objects.create(
                            wallet=main_wallet, amount=amount_conversion, transaction_type='withdrawal'
                        )
            return Response({"message": "Wallet will be debited as soon as an admin approves."},
                            status=status.HTTP_200_OK)
        except Wallet.DoesNotExist:
            return Response({"message": "This wallet does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'], permission_classes=[IsAdmin])
    def change_main_currency(self, request):
        try:
            wallet_id = request.data.get('wallet_id')
            currency = request.data.get('currency')
            main_wallet = Wallet.objects.get(id=wallet_id, main_wallet=True, owner__user_type='noob')
            main_wallet.balance = helpers.convert_balance(currency, main_wallet.currency, main_wallet.balance)
            main_wallet.currency = currency
            main_wallet.save()
            return Response({"message": "This main wallet has been updated."}, status=status.HTTP_200_OK)
        except Wallet.DoesNotExist:
            return Response({"message": "This wallet does not exist or is not a main wallet"},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TransactionViewSet(viewsets.ViewSet):
    queryset = Transaction.objects.all()

    @action(detail=False, permission_classes=[IsAdmin])
    def transaction_requests(self, request):
        try:
            transactions = Transaction.objects.all()
            serializer = TransactionSerializer(transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'], permission_classes=[IsAdmin])
    def approve_withdrawal(self, request):
        try:
            transaction_id = request.data.get('transaction_id')
            transaction = Transaction.objects.get(id=transaction_id)
            wallet = transaction.wallet
            wallet.balance = transaction.amount + wallet.balance
            transaction.is_approved = True
            wallet.save()
            transaction.save()
            return Response({"message": "Transaction approved successfully"}, status=status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            return Response({"message": "This transaction does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    