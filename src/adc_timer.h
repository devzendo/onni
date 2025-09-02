//------------------------------------------------------------------------------
//
// File        : adc_timer.h
// Description : 44.1kHz timer interrupt code
// License     : MIT License - see LICENSE.txt for more details
// Created     : 02/09/2025
//
// (C) 2025 Matt J. Gumbley
// matt.gumbley@devzendo.org
// http://devzendo.github.io/onni
//
//------------------------------------------------------------------------------

// Function pointer type for ADC callback
typedef void (*adc_callback_t)(uint16_t adc_value);

extern void set_adc_callback(adc_callback_t new_callback);
extern void setup_adc_timer();
extern int adc_pin();

