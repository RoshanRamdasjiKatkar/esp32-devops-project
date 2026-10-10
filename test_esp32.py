
import time
import serial
import pytest


PORT = "COM3"
BAUD_RATE = 115200


@pytest.fixture
def esp32():
    device = serial.Serial(
        port=PORT,
        baudrate=BAUD_RATE,
        timeout=2
    )

    # Allow ESP32 to restart after serial connection
    time.sleep(2)
    device.reset_input_buffer()

    yield device

    device.close()


def send_command(device, command):
    device.write((command + "\n").encode())
    device.flush()
    return device.readline().decode().strip()


def test_esp32_led_control(esp32):
    # Test LED ON
    assert send_command(esp32, "LEDON") == "OK:LEDON"
    assert send_command(esp32, "STATUS") == "STATUS:ON"

    # Test LED OFF
    assert send_command(esp32, "LEDOFF") == "OK:LEDOFF"
    assert send_command(esp32, "STATUS") == "STATUS:OFF"
