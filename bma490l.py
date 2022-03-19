import time
import smbus2

SENSOR_I2C_ADDR = 0x18

REG_CHIP_ID = 0x00
REG_ERR_REG = 0x02
REG_STATUS = 0x03
REG_DATA_0 = 0x0A
REG_DATA_1 = 0x0B
REG_DATA_2 = 0x0C
REG_DATA_3 = 0x0D
REG_DATA_4 = 0x0E
REG_DATA_5 = 0x0F
REG_DATA_6 = 0x10
REG_DATA_7 = 0x11
REG_DATA_8 = 0x12
REG_DATA_9 = 0x13
REG_DATA_10 = 0x14
REG_DATA_11 = 0x15
REG_DATA_12 = 0x16
REG_DATA_13 = 0x17
REG_SENSORTIME_0 = 0x18
REG_SENSORTIME_1 = 0x19
REG_SENSORTIME_2 = 0x1A
REG_EVENT = 0x1B
REG_INT_STATUS_0 = 0x1C
REG_INT_STATUS_1 = 0x1D
REG_TEMPERATURE = 0x22
REG_FIFO_LENGTH_0 = 0x24
REG_FIFO_LENGTH_1 = 0x25
REG_FIFO_DATA = 0x26
REG_INTERNAL_STATUS = 0x2A
REG_ACC_CONF = 0x40
REG_ACC_RANGE = 0x41
REG_AUX_CONF = 0x44
REG_FIFO_DOWNS = 0x45
REG_FIFO_WTM_0 = 0x46
REG_FIFO_WTM_1 = 0x47
REG_FIFO_CONFIG_0 = 0x48
REG_FIFO_CONFIG_1 = 0x49
REG_AUX_DEV_ID = 0x4B
REG_AUX_IF_CONF = 0x4C
REG_AUX_RD_ADDR = 0x4D
REG_AUX_WR_ADDR = 0x4E
REG_AUX_WR_DATA = 0x4F
REG_INT1_IO_CTRL = 0x53
REG_INT2_IO_CTRL = 0x54
REG_INT_LATCH = 0x55
REG_INT1_MAP = 0x56
REG_INT2_MAP = 0x57
REG_INT_MAP_DATA = 0x58
REG_INIT_CTRL = 0x59
REG_FEATURES_IN = 0x5E
REG_INTERNAL_ERROR = 0x5F
REG_NVM_CONF = 0x6A
REG_IF_CONF = 0x6B
REG_ACC_SELF_TEST = 0x6D
REG_NV_CONF = 0x70
REG_OFFSET_0 = 0x71
REG_OFFSET_1 = 0x72
REG_OFFSET_2 = 0x73
REG_PWR_CONF = 0x7C
REG_PWR_CTRL = 0x7D
REG_CMD = 0x7E

BMA490L_configuration = [ # taken from https://github.com/BoschSensortec/BMA490L-Sensor-API/blob/master/bma490l.c
	0xc8, 0x2e, 0x00, 0x2e, 0xc8, 0x2e, 0x00, 0x2e, 0xc8, 0x2e, 0x00, 0x2e, 0xc8, 0x2e, 0x00, 0x2e, 0xc8, 0x2e, 0x00,
	0x2e, 0xc8, 0x2e, 0x00, 0x2e, 0xc8, 0x2e, 0x00, 0x2e, 0x80, 0x2e, 0x58, 0x01, 0x80, 0x2e, 0x74, 0x02, 0xb0, 0xf0,
	0x10, 0x30, 0x21, 0x2e, 0x16, 0xf0, 0x80, 0x2e, 0xeb, 0x00, 0x19, 0x50, 0x17, 0x52, 0x01, 0x42, 0x3b, 0x80, 0x41,
	0x30, 0x01, 0x42, 0x3c, 0x80, 0x00, 0x2e, 0x01, 0x40, 0x01, 0x42, 0x21, 0x2e, 0xff, 0xaf, 0xb8, 0x2e, 0x9b, 0x95,
	0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18,
	0x00, 0x80, 0x2e, 0x18, 0x00, 0xfd, 0x2d, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x2e,
	0x55, 0xf0, 0xc0, 0x2e, 0x21, 0x2e, 0x55, 0xf0, 0x80, 0x2e, 0x18, 0x00, 0xfd, 0x2d, 0xaa, 0x00, 0x05, 0x00, 0xaa,
	0x00, 0x05, 0x00, 0x40, 0x48, 0x88, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x98, 0x2e, 0x80, 0x00, 0x20, 0x26, 0x98, 0x2e, 0xef, 0x00, 0x10, 0x30, 0x21, 0x2e,
	0x59, 0xf0, 0x98, 0x2e, 0x38, 0x00, 0x98, 0x2e, 0x7f, 0x01, 0x98, 0x2e, 0x8e, 0x01, 0x00, 0x2e, 0x00, 0x2e, 0xd0,
	0x2e, 0x98, 0x2e, 0xce, 0x00, 0x01, 0x2e, 0x34, 0x00, 0x00, 0xb2, 0x0d, 0x2f, 0x00, 0x30, 0x21, 0x2e, 0x34, 0x00,
	0x01, 0x50, 0x98, 0x2e, 0x13, 0x01, 0x01, 0x50, 0x03, 0x52, 0x98, 0x2e, 0x00, 0xb0, 0x01, 0x50, 0x05, 0x52, 0x98,
	0x2e, 0x00, 0xb0, 0x98, 0x2e, 0x38, 0x00, 0xe6, 0x2d, 0x13, 0x52, 0x40, 0x30, 0x42, 0x40, 0x90, 0x0a, 0x42, 0x42,
	0x58, 0x84, 0x07, 0x52, 0xa1, 0x42, 0x71, 0x3c, 0x09, 0x56, 0x83, 0x42, 0xa9, 0x84, 0x83, 0x32, 0x84, 0x40, 0x61,
	0x08, 0x4b, 0x0a, 0x81, 0x42, 0x82, 0x82, 0x02, 0x3f, 0x43, 0x40, 0x9a, 0x08, 0x52, 0x42, 0x40, 0x42, 0x7e, 0x80,
	0x61, 0x30, 0x01, 0x42, 0x10, 0x50, 0x01, 0x2e, 0x40, 0xf0, 0x1a, 0x90, 0xfb, 0x7f, 0x20, 0x2f, 0x03, 0x30, 0x0d,
	0x50, 0x34, 0x33, 0x06, 0x30, 0x11, 0x52, 0x0b, 0x54, 0x55, 0x32, 0x1d, 0x1a, 0xe3, 0x22, 0x18, 0x1a, 0x0f, 0x58,
	0xe3, 0x22, 0x04, 0x30, 0xd5, 0x40, 0xb5, 0x0d, 0xe1, 0xbe, 0x6f, 0xbb, 0x80, 0x91, 0xa9, 0x0d, 0x01, 0x89, 0xb5,
	0x23, 0x10, 0xa1, 0xf7, 0x2f, 0xda, 0x0e, 0x34, 0x33, 0xeb, 0x2f, 0x01, 0x2e, 0x25, 0x00, 0x70, 0x1a, 0x00, 0x30,
	0x21, 0x30, 0x02, 0x2c, 0x08, 0x22, 0x30, 0x30, 0x00, 0xb2, 0x06, 0x2f, 0x21, 0x2e, 0x59, 0xf0, 0x98, 0x2e, 0x38,
	0x00, 0x00, 0x2e, 0x00, 0x2e, 0xd0, 0x2e, 0xfb, 0x6f, 0xf0, 0x5f, 0xb8, 0x2e, 0x1d, 0x50, 0x05, 0x2e, 0x00, 0xf0,
	0x17, 0x56, 0xd3, 0x0f, 0x01, 0x40, 0xf4, 0x33, 0xcc, 0x08, 0x0d, 0x2f, 0xf4, 0x30, 0x94, 0x08, 0xb9, 0x88, 0x02,
	0xa3, 0x04, 0x2f, 0x1b, 0x58, 0x4c, 0x0a, 0x87, 0xa2, 0x05, 0x2c, 0xcb, 0x22, 0x17, 0x54, 0x4a, 0x0a, 0xf2, 0x3b,
	0xca, 0x08, 0x3c, 0x80, 0x27, 0x2e, 0x59, 0xf0, 0x01, 0x40, 0x01, 0x42, 0xb8, 0x2e, 0x1a, 0x24, 0x26, 0x00, 0x80,
	0x2e, 0x58, 0x00, 0x00, 0x31, 0xc0, 0x2e, 0x21, 0x2e, 0xba, 0xf0, 0x12, 0x30, 0x12, 0x42, 0x02, 0x30, 0x12, 0x42,
	0x12, 0x42, 0x12, 0x42, 0x02, 0x42, 0x03, 0x80, 0x41, 0x84, 0x11, 0x42, 0x02, 0x42, 0xb8, 0x2e, 0x44, 0x47, 0x35,
	0x00, 0x46, 0x00, 0x4f, 0x00, 0xaf, 0x00, 0xff, 0x00, 0xff, 0xb7, 0x00, 0x02, 0x00, 0xb0, 0x05, 0x80, 0xb1, 0xf0,
	0x88, 0x00, 0x80, 0x00, 0x5e, 0xf0, 0xc0, 0x00, 0x59, 0xf0, 0x89, 0xf0, 0x38, 0x00, 0x40, 0x00, 0x42, 0x00, 0x60,
	0x50, 0x03, 0x2e, 0x45, 0x00, 0xe0, 0x7f, 0xf1, 0x7f, 0xdb, 0x7f, 0x30, 0x30, 0x15, 0x54, 0x0a, 0x1a, 0x28, 0x2f,
	0x1a, 0x25, 0x7a, 0x82, 0x00, 0x30, 0x43, 0x30, 0x32, 0x30, 0x05, 0x30, 0x04, 0x30, 0xf6, 0x6f, 0xf2, 0x09, 0xfc,
	0x13, 0xc2, 0xab, 0xb3, 0x09, 0xef, 0x23, 0x80, 0xb3, 0xe6, 0x6f, 0xb7, 0x01, 0x00, 0x2e, 0x8b, 0x41, 0x4b, 0x42,
	0x03, 0x2f, 0x46, 0x40, 0x86, 0x17, 0x81, 0x8d, 0x46, 0x42, 0x41, 0x8b, 0x23, 0xbd, 0xb3, 0xbd, 0x03, 0x89, 0x41,
	0x82, 0x07, 0x0c, 0x43, 0xa3, 0xe6, 0x2f, 0xe1, 0x6f, 0xa2, 0x6f, 0x52, 0x42, 0x00, 0x2e, 0xb2, 0x6f, 0x52, 0x42,
	0x00, 0x2e, 0xc2, 0x6f, 0x42, 0x42, 0x03, 0xb2, 0x06, 0x2f, 0x01, 0x2e, 0x59, 0xf0, 0x01, 0x32, 0x01, 0x0a, 0x21,
	0x2e, 0x59, 0xf0, 0x06, 0x2d, 0x01, 0x2e, 0x59, 0xf0, 0xf1, 0x3d, 0x01, 0x08, 0x21, 0x2e, 0x59, 0xf0, 0xdb, 0x6f,
	0xa0, 0x5f, 0xb8, 0x2e, 0x60, 0x50, 0xc3, 0x7f, 0xd4, 0x7f, 0xe7, 0x7f, 0xf6, 0x7f, 0xb2, 0x7f, 0xa5, 0x7f, 0x36,
	0x30, 0x07, 0x2e, 0x01, 0xf0, 0xbe, 0xbd, 0xbe, 0xbb, 0x1f, 0x58, 0x77, 0x05, 0x01, 0x56, 0x21, 0x54, 0x27, 0x41,
	0x06, 0x41, 0xf8, 0xbf, 0xbe, 0x0b, 0xb5, 0x11, 0xd6, 0x42, 0x03, 0x89, 0x5a, 0x0e, 0xf6, 0x2f, 0x12, 0x30, 0x25,
	0x2e, 0x34, 0x00, 0x02, 0x31, 0x25, 0x2e, 0xb8, 0xf0, 0xd4, 0x6f, 0xc3, 0x6f, 0xe7, 0x6f, 0xb2, 0x6f, 0xa5, 0x6f,
	0xf6, 0x6f, 0xa0, 0x5f, 0xc8, 0x2e, 0x10, 0x50, 0x23, 0x52, 0x03, 0x50, 0xfb, 0x7f, 0x98, 0x2e, 0xf3, 0x00, 0x03,
	0x52, 0x45, 0x82, 0x10, 0x30, 0x50, 0x42, 0x60, 0x30, 0xfb, 0x6f, 0xc0, 0x2e, 0x40, 0x42, 0xf0, 0x5f, 0x10, 0x50,
	0x25, 0x52, 0x05, 0x50, 0xfb, 0x7f, 0x98, 0x2e, 0xf3, 0x00, 0x05, 0x52, 0x45, 0x82, 0x00, 0x30, 0x50, 0x42, 0x70,
	0x30, 0xfb, 0x6f, 0xc0, 0x2e, 0x40, 0x42, 0xf0, 0x5f, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e,
	0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80,
	0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00,
	0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18,
	0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e,
	0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80,
	0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00,
	0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18,
	0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e,
	0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80,
	0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0x80, 0x2e, 0x18, 0x00, 0xfd, 0x2d, 0x46, 0x86,
	0x70, 0x50, 0xe5, 0x40, 0xc3, 0x88, 0x42, 0x84, 0x04, 0x41, 0xc3, 0x40, 0x06, 0x41, 0x6d, 0xbb, 0xc2, 0x7f, 0xf5,
	0x7f, 0x80, 0xb3, 0xe6, 0x7f, 0xd0, 0x7f, 0xb3, 0x7f, 0x12, 0x30, 0x5e, 0x2f, 0x31, 0x25, 0x55, 0x40, 0x41, 0x91,
	0xa1, 0x7f, 0x0f, 0x2f, 0x01, 0x30, 0xc1, 0x42, 0x00, 0x2e, 0xc2, 0x6f, 0x13, 0x40, 0x93, 0x42, 0x00, 0x2e, 0x13,
	0x40, 0x93, 0x42, 0x00, 0x2e, 0x00, 0x40, 0x80, 0x42, 0xbd, 0x80, 0xc0, 0x2e, 0x01, 0x42, 0x90, 0x5f, 0xc7, 0x86,
	0x01, 0x30, 0xc5, 0x40, 0xfb, 0x86, 0x45, 0x41, 0x04, 0x41, 0x43, 0xbe, 0xc3, 0xbb, 0xd5, 0xbe, 0x55, 0xba, 0x97,
	0x7f, 0x05, 0x30, 0xd1, 0x15, 0xf7, 0x09, 0xc0, 0xb3, 0x09, 0x2f, 0x06, 0x40, 0xc7, 0x40, 0xb7, 0x05, 0x07, 0x30,
	0x80, 0xa9, 0xfe, 0x05, 0xb7, 0x23, 0x74, 0x0f, 0x55, 0x23, 0xe6, 0x6f, 0x41, 0x82, 0x01, 0x80, 0xc1, 0x86, 0x43,
	0xa2, 0xec, 0x2f, 0xb0, 0x6f, 0xa4, 0x6f, 0x28, 0x1a, 0xd1, 0x6f, 0xc3, 0x6f, 0x02, 0x2f, 0x02, 0x30, 0x18, 0x2c,
	0x02, 0x43, 0x05, 0x41, 0x6a, 0x29, 0x96, 0x6f, 0x05, 0x43, 0x6e, 0x0e, 0x10, 0x2f, 0xf4, 0x6f, 0x00, 0xb3, 0x03,
	0x2f, 0x3f, 0x89, 0x94, 0x14, 0x25, 0x2e, 0x5e, 0xf0, 0x41, 0x25, 0x23, 0x25, 0x15, 0x41, 0x95, 0x42, 0x00, 0x2e,
	0x15, 0x41, 0x95, 0x42, 0x00, 0x2e, 0x04, 0x41, 0x84, 0x42, 0x00, 0x90, 0x09, 0x2f, 0x50, 0x40, 0xd0, 0x42, 0x00,
	0x2e, 0x50, 0x40, 0xd0, 0x42, 0x00, 0x2e, 0x40, 0x40, 0x02, 0x2c, 0xc0, 0x42, 0x42, 0x42, 0x90, 0x5f, 0xb8, 0x2e,
	0x00, 0x2e, 0x10, 0x24, 0x8a, 0x02, 0x11, 0x24, 0x00, 0x0c, 0x12, 0x24, 0x80, 0x2e, 0x13, 0x24, 0x18, 0x00, 0x12,
	0x42, 0x13, 0x42, 0x41, 0x1a, 0xfb, 0x2f, 0x10, 0x24, 0x50, 0x39, 0x11, 0x24, 0x21, 0x2e, 0x21, 0x2e, 0x10, 0x00,
	0x23, 0x2e, 0x11, 0x00, 0x80, 0x2e, 0x10, 0x00
]

BMA480L_acc_ranges = {2: 0b00, 4: 0b01, 8: 0b10, 16: 0b11}


def twos_complement(value, bits):
	if(value & (1 << (bits - 1))) != 0:
		value = value - (1 << bits)
	return value

def read_value(register):
	value = bus.read_i2c_block_data(SENSOR_I2C_ADDR, register, 1)
	return value[0]

def read_value_double(register):
	value = bus.read_i2c_block_data(SENSOR_I2C_ADDR, register, 2)
	return (value[1] << 8) | value[0]

def write_value(register, value):
	bus.write_i2c_block_data(SENSOR_I2C_ADDR, register, [value])
	time.sleep(0.1)

def set_configuration_bits(configuration, value, shift, bitsCount):
	clearBits = 0;
	i = 0
	while(i < bitsCount):
		clearBits |= (1 << i)
		i += 1

	return (configuration & ~(clearBits << shift)) | (value << shift);

def print_register(register):
	print(hex(register) + ": " + str(read_value(register)))

def convert_temperature(raw_value):
	if raw_value == 0x80:
		return None
	return twos_complement(raw_value, 8) + 23

def convert_acceleration(raw_value):
	return twos_complement(raw_value, 16) / (32768 / sensor_range)


sensor_range = 2 # 2|4|8|16
sensor_odr = 0x08 # 0x06 = 25 Hz, 0x08 = 100 Hz, 0x0C = 1600 Hz (for more values see table acc_odr on page 56 in data sheet)


bus = smbus2.SMBus(1)

if read_value(REG_CHIP_ID) == 0x1A:
	print("Sensor BMA490L found")
else:
	print("Sensor not found")
	exit()


# initialisation

try:
	write_value(REG_CMD, 0xB6) # soft reset (may throw exception)
except:
	None

time.sleep(0.1)

write_value(REG_PWR_CONF, 0b0)

write_value(REG_INIT_CTRL, 0b0)

msg_write = smbus2.i2c_msg.write(SENSOR_I2C_ADDR, [REG_FEATURES_IN] + BMA490L_configuration)
bus.i2c_rdwr(msg_write)

"""
# read configuration back
msg_write = smbus2.i2c_msg.write(SENSOR_I2C_ADDR, [REG_FEATURES_IN])
msg_read = smbus2.i2c_msg.read(SENSOR_I2C_ADDR, len(BMA490L_configuration))
bus.i2c_rdwr(msg_write, msg_read)

print(list(msg_read) == BMA490L_configuration)
"""

write_value(REG_INIT_CTRL, 0b1)
time.sleep(0.2)

if read_value(REG_INTERNAL_STATUS) != 0b1:
	print("Sensor failed to initialise")
	exit()

write_value(REG_ACC_RANGE, BMA480L_acc_ranges[sensor_range]) # set range

write_value(REG_ACC_CONF, 0b10100000 | sensor_odr) # set ODR

write_value(REG_PWR_CTRL, 0b100) # enable accelerometer


while True:
	print("")
	print("T: {}".format(convert_temperature(read_value(REG_TEMPERATURE))))
	print("x: {:.4f}".format(convert_acceleration(read_value_double(REG_DATA_8))))
	print("y: {:.4f}".format(convert_acceleration(read_value_double(REG_DATA_10))))
	print("z: {:.4f}".format(convert_acceleration(read_value_double(REG_DATA_12))))
	time.sleep(1)
