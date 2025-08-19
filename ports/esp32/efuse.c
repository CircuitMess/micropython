#include "py/obj.h"
#include "py/objstr.h"
#include "py/runtime.h"
#include "esp_efuse.h"

static esp_efuse_desc_t PIDBlock = {EFUSE_BLK3, 16, 16};
static const esp_efuse_desc_t *PID_Blob[] = {&PIDBlock, NULL};


/**
 * Revision number is on different locations depending on ESP32 version.
 *
 * 	ESP32: block3, bits 0-7
 * 	ESP32-S3: block3, bits 32-39
 *
 */
#if CONFIG_IDF_TARGET_ESP32S3

static esp_efuse_desc_t RevBlock = {EFUSE_BLK3, 32, 8};

#elif CONFIG_IDF_TARGET_ESP32

static esp_efuse_desc_t RevBlock = {EFUSE_BLK3, 0, 8};

#endif

static const esp_efuse_desc_t *Rev_Blob[] = {&RevBlock, NULL};

mp_obj_t read_pid(){
	uint16_t pid = 0;

	const esp_err_t err = esp_efuse_read_field_blob((const esp_efuse_desc_t **) PID_Blob, &pid, 16);
	if(err != ESP_OK){
		mp_raise_ValueError(MP_ERROR_TEXT("efuse read error"));
		return MP_OBJ_NEW_SMALL_INT(0);
	}

	return MP_OBJ_NEW_SMALL_INT(pid);
}

STATIC MP_DEFINE_CONST_FUN_OBJ_0(read_pid_obj, read_pid);

mp_obj_t read_rev(){
	uint8_t rev = 0;

	const esp_err_t err = esp_efuse_read_field_blob((const esp_efuse_desc_t **) Rev_Blob, &rev, 8);
	if(err != ESP_OK){
		mp_raise_ValueError(MP_ERROR_TEXT("efuse read error"));
		return MP_OBJ_NEW_SMALL_INT(0);
	}

	return MP_OBJ_NEW_SMALL_INT(rev);
}

STATIC MP_DEFINE_CONST_FUN_OBJ_0(read_rev_obj, read_rev);

mp_obj_t read_reg(mp_obj_t block, mp_obj_t reg){
	uint32_t readReg = esp_efuse_read_reg(mp_obj_get_int(block), mp_obj_get_int(reg));

	return MP_OBJ_NEW_SMALL_INT(readReg);
}

STATIC MP_DEFINE_CONST_FUN_OBJ_2(read_reg_obj, read_reg);

static const mp_rom_map_elem_t mp_module_efuse_globals_table[] = {
		{MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_efuse)},
		{MP_ROM_QSTR(MP_QSTR_read_pid), MP_ROM_PTR(&read_pid_obj)},
		{MP_ROM_QSTR(MP_QSTR_read_rev), MP_ROM_PTR(&read_rev_obj)},
		{MP_ROM_QSTR(MP_QSTR_read_reg), MP_ROM_PTR(&read_reg_obj)},
};
static MP_DEFINE_CONST_DICT(mp_module_efuse_globals, mp_module_efuse_globals_table);

const mp_obj_module_t mp_module_efuse = {
		.base = {&mp_type_module},
		.globals = (mp_obj_dict_t *) &mp_module_efuse_globals,
};

MP_REGISTER_MODULE(MP_QSTR_efuse, mp_module_efuse);