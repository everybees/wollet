from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from api.models import Transaction, User, Wallet
from api.serializers import UserSerializer, WalletSerializer
from permissions import ActionBasedPermission, IsAdmin, IsElite
from rest_framework.permissions import AllowAny, IsAuthenticated
import helpers


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        AllowAny: ['create'],
        IsAuthenticated: ['retrieve', 'list']
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

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def fund_wallet(self, request):
        data = request.data
        amount = data.get('amount', 0)
        currency = data.get('currnecy', "NGN")
        wallet_id = data.get('wallet_id', None)
        try:
            token = Token.objects.get(key=request.auth.key)
            user_type = token.user.user_type
            if user_type != "admin":
                if user_type == 'noob':
                    wallet = Wallet.objects.get(id=wallet_id)
                    helpers.convert_to_main_currency(amount, currency, wallet, 'funding')
            else:
                helpers.perform_funding(amount, currency, wallet_id)
                return Response({"message": "Wallet funded successfully"}, status=status.HTTP_200_OK)
            return Response({"message": "Wallet will be funded as soon as an admin approves."}, status=status.HTTP_200_OK)
        except Wallet.DoesNotExist:
            return Response({"message": "This wallet does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def withdraw(self, request):
        data = request.data
        amount = data.get('amount', 0),
        currency = data.get('currnecy', "NGN")
        wallet_id = data.get('wallet_id', None)
        try:
            token = Token.objects.get(key=request.auth.key)
            user_type = token.user.user_type
            if user_type != 'admin':
                wallet = Wallet.objects.get(id=wallet_id)
                helpers.convert_to_main_currency(amount, currency, wallet, 'withdrawal')
            return Response({"message": "Wallet will be debited as soon as an admin approves."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()

    @action(detail=False, permission_classes=[IsAdmin])
    def transaction_requests(self, request):
        ...

    @action(detail=False, methods=['put'], permission_classes=[IsAdmin])
    def approve_withdrawal(self, request):
        try:
            ...
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    