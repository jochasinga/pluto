BOARDS = {
    'arduino' : {
        'digital' : tuple(x for x in range(14)),
        'analog' : tuple(x for x in range(6)),
        'pwm' : (3, 5, 6, 9, 10, 11),
        'use_ports' : True,
        'disabled' : (0, 1) # Rx, Tx, Crystal
    },
    'arduino_mega' : {
        'digital' : tuple(x for x in range(54)),
        'analog' : tuple(x for x in range(16)),
        'pwm' : tuple(x for x in range(2,14)),
        'use_ports' : True,
        'disabled' : (0, 1) # Rx, Tx, Crystal
    },
    'arduino_due': {
        'digital': tuple(x for x in range(54)),
        'analog': tuple(x for x in range(12)),
        'pwm': tuple(x for x in range(2, 14)),
        'use_ports': True,
        'disabled': (0, 1)  # Rx, Tx, Crystal
    },
    'arduino_yun' : {
        'digital' : tuple(x for x in range(20)),
        'analog' : tuple(x for x in range(14, 19)),
        'pwm' : (3, 5, 6, 9, 10, 11),
        'use_ports' : True,
        'disabled' : (0, 1) # Rx, Tx, Crystal
    },
    'spark_core' : {
        'digital' : tuple(x for x in range(7)),
        'analog' : tuple(x for x in range(10, 17)),
        'pwm' : (0, 1, 10, 11, 14, 15, 16, 17),
        'use_ports' : True,
        'disabled' : (18, 19)
    },
    'arduino_lilypad' : {
        'digital' : tuple(x for x in range(4)),
        'analog' : tuple(x for x in range(16, 21)),
        'pwm' : (3, 7, 8, 11, 12, 13),
        'use_ports' : True,
        'disabled' : (0, 1) # Rx, Tx, Crystal
    }
}
