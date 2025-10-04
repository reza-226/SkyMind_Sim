# D:\Payannameh\SkyMind_Sim\skymind_sim\network\communication.py
import math
import random
import time

class UAVCommChannel:
    """
    شبیه‌ساز انتزاعی کانال ارتباطی پهپادها
    """
    def __init__(self, comm_range=100.0, bandwidth=1_000_000, packet_loss_rate=0.01, base_latency=0.05):
        self.comm_range = comm_range      # متر
        self.bandwidth = bandwidth        # بیت بر ثانیه
        self.packet_loss_rate = packet_loss_rate
        self.base_latency = base_latency  # ثانیه

    def in_range(self, pos1, pos2):
        """بررسی در برد بودن دو پهپاد"""
        return math.dist(pos1, pos2) <= self.comm_range

    def transmit(self, sender, receiver, data_size_bytes):
        """
        ارسال پیام بین پهپادها
        """
        if not self.in_range(sender.position, receiver.position):
            return False, "Out of range"

        if random.random() < self.packet_loss_rate:
            return False, "Packet lost"

        # محاسبه تاخیر کلی
        tx_time = data_size_bytes / self.bandwidth
        total_latency = self.base_latency + tx_time

        # شبیه سازی تاخیر (اختیاری برای سرعت اجرا)
        time.sleep(total_latency)

        return True, total_latency


class UAVNetworkManager:
    """
    مدیریت شبکه بین پهپادها: آپدیت جدول همسایگانی و ارسال پیام‌ها
    """
    def __init__(self, drones, channel: UAVCommChannel):
        self.drones = drones
        self.channel = channel

    def update_neighbors(self):
        """آپدیت جدول همسایگی همه پهپادها"""
        for drone in self.drones:
            drone.neighbors = [
                other.id for other in self.drones
                if other.id != drone.id and self.channel.in_range(drone.position, other.position)
            ]

    def broadcast(self, sender_id, msg, size_bytes=1024):
        """ارسال پیام Broadcast به همه همسایه‌ها از یک پهپاد"""
        sender = next((d for d in self.drones if d.id == sender_id), None)
        if not sender:
            return

        for neighbor_id in sender.neighbors:
            receiver = next((d for d in self.drones if d.id == neighbor_id), None)
            success, latency = self.channel.transmit(sender, receiver, size_bytes)
            receiver.receive_message(msg, latency, success)
