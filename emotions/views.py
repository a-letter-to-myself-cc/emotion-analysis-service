import json
import requests
import pika
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reanalyze_all_emotions(request):
    """편지 가져와서 MQ로 발행"""
    # ✅ 토큰 추출
    auth_header = request.META.get("HTTP_AUTHORIZATION")
    if not auth_header or not auth_header.startswith("Bearer "):
        return Response({"error": "인증 토큰이 없습니다."}, status=401)

    token = auth_header.split("Bearer ")[1]

    try:
        # 1. 편지 가져오기
        response = requests.get(
            "http://letter-service:8006/api/letters/",
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        letters_data = response.json()[:5]

        # 2. MQ 발행
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        channel.exchange_declare(exchange='emotion.direct', exchange_type='direct')

        for letter in letters_data:
            message = {
                "letter_id": letter["id"],
                "content": letter["content"]
            }
            channel.basic_publish(
                exchange='emotion.direct',
                routing_key='analyze',
                body=json.dumps(message),
            )

        connection.close()

        return Response({"status": "success", "published_count": len(letters_data)})

    except requests.RequestException as e:
        return Response({"error": "편지를 불러오는 데 실패했습니다", "details": str(e)}, status=500)

    except pika.exceptions.AMQPError as e:
        return Response({"error": "RabbitMQ 발행 실패", "details": str(e)}, status=500)
