import csv
import io

import pytest

from app.services.bom_parser import BOMParser


@pytest.fixture
def sample_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Part Number", "Manufacturer", "Qty", "Description"])
    writer.writerow(["STM32F103C8T6", "STMicroelectronics", "10", "ARM Cortex-M3 MCU"])
    writer.writerow(["ESP32-WROOM-32", "Espressif", "5", "WiFi/BLE Module"])
    writer.writerow(["LM358P", "Texas Instruments", "20", "Dual Op-Amp"])
    return output.getvalue().encode("utf-8")


@pytest.fixture
def parser():
    return BOMParser()


def test_parse_csv_bom(parser, sample_csv):
    items = parser.parse(sample_csv, "bom.csv")
    assert len(items) == 3
    assert items[0]["raw_part_number"] == "STM32F103C8T6"
    assert items[0]["manufacturer"] == "STMicroelectronics"
    assert items[0]["quantity"] == 10


def test_parse_skips_empty_rows(parser):
    data = b"part number,manufacturer\nSTM32F103C8T6,ST\n,,\nESP32,Espressif\n"
    items = parser.parse(data, "test.csv")
    assert len(items) == 2


def test_parse_handles_column_aliases(parser):
    data = b"MPN,Mfr,Qty.\nSTM32F103C8T6,ST,10\n"
    items = parser.parse(data, "test.csv")
    assert len(items) == 1
    assert items[0]["manufacturer"] == "ST"


def test_parse_invalid_format(parser):
    with pytest.raises(ValueError):
        parser.parse(b"random data", "test.txt")


def test_parse_missing_mpn_column_raises(parser):
    data = b"foo,bar\n1,2\n"
    with pytest.raises(ValueError, match="Could not find a part number column"):
        parser.parse(data, "test.csv")
