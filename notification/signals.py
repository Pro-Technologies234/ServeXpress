
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import  Notification 
from core.models import Proposal, Review, Job, DeliveryRequest, QRScan

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import datetime


def send_realtime_notification(user, title,message):
    """
    Save the notification to the DB and send it over WebSocket.
    """
    Notification.objects.create(user=user, title=title, message=message)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "send_notification",
            "title": title,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@receiver(post_save, sender=Proposal)
def notify_proposal_created(sender, instance, created, **kwargs):
    if created:
        send_realtime_notification(
            instance.job.client,
            "Recieved Proposal.",
            f"{instance.freelancer.username} submitted a proposal for '{instance.job.title}'."
        )


@receiver(post_save, sender=Review)
def notify_review_created(sender, instance, created, **kwargs):
    if created:
        send_realtime_notification(
            instance.freelancer,
            "Recieved Review.",
            f"You received a review with {instance.rating} star(s)."
        )


@receiver(post_save, sender=Job)
def notify_job_assigned(sender, instance, **kwargs):
    if instance.is_assigned and instance.freelancer:
        send_realtime_notification(
            instance.freelancer,
            "Proposal Accepted🎉.",
            f"You have been assigned to the job: '{instance.title}'."
        )


@receiver(post_save, sender=DeliveryRequest)
def notify_delivery_assigned(sender, instance, **kwargs):
    if instance.assigned_to:
        send_realtime_notification(
            instance.assigned_to,
            "Delivery Assigned.",
            f"You’ve been assigned to a delivery to: {instance.dropoff_address}."
        )


@receiver(post_save, sender=QRScan)
def notify_qr_scanned(sender, instance, created, **kwargs):
    if created:
        scan_action = instance.scan_type.capitalize()
        send_realtime_notification(
            "QR code scan",
            instance.delivery.client,
            f"{scan_action} scan by {instance.scanned_by.username} for your delivery."
        )