#include "cm_boards.h"
#include "driver/gpio.h"

#ifdef CONFIG_IDF_TARGET_ESP32S3

static void init_artemis(){
	static const gpio_num_t PWDN = GPIO_NUM_42;
	static const gpio_num_t LEDs[] = { 17, 18, 43, 44, 45, 46 };

	for(int i = 0; i < sizeof(LEDs)/sizeof(LEDs[0]); i++){
		const gpio_num_t pin = LEDs[i];
		const gpio_config_t cfg_led = {
				.pin_bit_mask = 1ULL << pin,
				.mode = GPIO_MODE_OUTPUT,
				.pull_up_en = 0,
				.pull_down_en = 0,
				.intr_type = 0
		};
		gpio_config(&cfg_led);
		gpio_set_level(pin, 0);
	}

	const gpio_config_t cfg_pwdn = {
			.pin_bit_mask = 1ULL << PWDN,
			.mode = GPIO_MODE_INPUT,
			.pull_up_en = 0,
			.pull_down_en = 0,
			.intr_type = 0
	};
	gpio_config(&cfg_pwdn);
}

static void init_perse_rover(){
	// Set Power LED to ON
}

static void init_perse_missionctrl(){
	// Set Power LED to ON
}

#elifdef CONFIG_IDF_TARGET_ESP32

#endif

void cm_boards_init(){
	// TODO: efuse check board

#ifdef CONFIG_IDF_TARGET_ESP32S3
	if(0){
		init_artemis();
	}
#elifdef CONFIG_IDF_TARGET_ESP32

#endif
}