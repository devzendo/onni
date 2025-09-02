//------------------------------------------------------------------------------
//
// File        : adc_timer.c
// Description : 44.1kHz timer interrupt code
// License     : MIT License - see LICENSE.txt for more details
// Created     : 02/09/2025
//
// (C) 2025 Matt J. Gumbley
// matt.gumbley@devzendo.org
// http://devzendo.github.io/onni
//
//------------------------------------------------------------------------------

#include "pico/stdlib.h"

#include "hardware/gpio.h"
#include "hardware/adc.h"
#include "hardware/timer.h"
#include "hardware/irq.h"

#include "adc_timer.h"

// Define the ADC pin (GPIO 26 = ADC0, GPIO 27 = ADC1, GPIO 28 = ADC2, GPIO 29 = ADC3)
#define ADC_PIN 26
#define ADC_CHANNEL 0  // ADC0 corresponds to GPIO 26

// Global function pointer
adc_callback_t g_adc_callback = NULL;

// Timer interrupt period for 44.1kHz (approximately 22.676 microseconds)
// Timer runs at 1MHz, so we need 22.676 timer ticks
#define TIMER_PERIOD_US 22676  // Microseconds for 44.1kHz

// Alarm number to use (0-3 available)
#define ALARM_NUM 0


// Timer interrupt service routine
int64_t timer_callback(alarm_id_t id, void *user_data) {
  // Read from ADC.
  uint16_t adc_result = adc_read();
    
  // Call the configured function pointer if it's set...
  if (g_adc_callback != NULL) {
    g_adc_callback(adc_result);
  }
    
  // Return the period in microseconds to automatically reschedule
  // Returning a positive value reschedules the alarm
  return TIMER_PERIOD_US;
}

// Function to set the ADC callback
void set_adc_callback(adc_callback_t callback) {
  g_adc_callback = callback;
}

// Initialize ADC and timer
void setup_adc_timer() {
  // Initialize ADC
  adc_init();

  // Configure ADC pin
  adc_gpio_init(ADC_PIN);

  // Select ADC channel
  adc_select_input(ADC_CHANNEL);

  // Set up the timer alarm for 44.1kHz sampling
  // add_alarm_in_us will automatically handle the timer setup
  add_alarm_in_us(TIMER_PERIOD_US, timer_callback, NULL, true);
}

// Obtain ADC pin
int adc_pin() {
  return ADC_PIN;
}
