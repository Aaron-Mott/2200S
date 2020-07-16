# -*- coding: utf-8 -*-
"""
Created on Thu May 28 08:20:13 2020

@author: Aaron Mott
aaron.b.mott@gmail.com
"""

import visa

class KEI2220S():
    
    def __innit__(self,
                  inst_address,
                  baud_rate = 9600,
                  term_chars = '\n',
                  timeout = 2000):
        """
        Initializes the instrument with instrument address, baud rate,
        termination characters, and timeout.

        Parameters
        ----------
        inst_address : str
            The port address of the instrument.
        baud_rate : int, optional
             The default is 9600, but may be set to 4800, 9600, 19200, 38400,
                                                    57600, or 115200.
        term_chars : str, optional
            The termination character for the instrument.
        timeout : int, float
            Amount of time to wait for a response before a timeout error in
            milliseconds.
        """
        self.rm = visa.ResourceManager()
        self.inst = self.rm.open_resource(self.instr_address,
                                          baud_rate,
                                          term_chars,
                                          timeout)
        
    def clear_status(self):
        """Clears all the event registers and error queue."""
        self.inst.write("*CLS")
        
    def set_beep(self, boolean):
        """
        Turns the key beep sound on or off.

        Parameters
        ----------
        boolean : str, int
            The state of the beep.
        """
        if str(boolean).upper() in ['0', '1', 'ON', 'OFF']:
            self.inst.write(f"CONF:SOUND {boolean}.upper()")
        if int(boolean) in range(2):
            self.inst.write(f"CONF:SOUND {boolean}")
        else:
            raise ValueError("Value Error. Please enter 0, 1, ON, or OFF.")
        
    def get_beep(self):
        """Returns status of the key beep sound."""
        beep = str(self.inst.query("CONF:SOUND?"))
        return(beep)
    
    def set_ese(self, NR1):
        """
        Sets and queries the bits in the Event Status Enable Register.

        Parameters
        ----------
        NR1 : int
            Bit of the Even Status Enable Register.
        """
        if int(NR1) in range(256):
            self.inst.write(f"*ESE {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 0 "
                             "and 255.")
        
    def get_ese(self):
        """Returns the bits in the Event Status Enable Register."""
        ese = str(self.inst.query("*ESE?"))
        return(ese)
    
    def get_esr(self):
        """Returns the contents of the Standard Event Status Register."""
        esr = str(self.inst.query("*ESR"))
        return(esr)

    def get_last_curr(self):
        """
        Returns the last measured output current stored in the communications
        buffer of the power supply. A new measurement is not initiated by
        this command.
        """
        last_curr = str(self.inst.query("FETC:CURR?"))
        return(last_curr)
      
    def get_last_volt(self):
        """
        Returns the last measured output voltage stored in the communications
        buffer of the power supply. A new measurement is not initiated by
        this command.
        """
        last_volt = str(self.inst.query("FETC:VOLT?"))
        return(last_volt)   

    def get_last_power(self):
        """
        Returns the last measured output current stored in the communications
        buffer of the power supply. A new measurement is not initiated by
        this command. The power calculation in the instrument is performed
        approximately every 100 ms. Ensure that the voltage and current are
        stable longer than this for good results.
        """
        last_power = str(self.inst.query("FETCh:POW?"))
        return(last_power)
    
    def get_info(self):
        """
        Returns the power supply identification code in IEEE 488.2 notation.
        """
        info = str(self.inst.query("*IDN?")).split(',')
        return(" Manufacturer: " + info[0] + '\n',
              "Model: " + info[1] + '\n',
              "Serial Number: " + info[2]+'\n',
              " Firmware Version: " + info[3])
    
    def get_model(self):
        """Returns model number of the power supply."""
        model = str(self.inst.query("*IDN").split(',')[1].replace(' ',''))
        return(model)
         
    def get_curr(self):
        """
        Initiates and executes a new current measurement, and returns the
        measured output current of the power supply.
        """
        curr = str(self.inst.query("MEAS:CURR?"))
        return(curr)
    
    def get_volt(self):
        """
        Initiates and executes a new voltage measurement, and returns the
        measured output voltage of the power supply.
        """
        volt = str(self.inst.query("MEAS:VOLT?"))
        return(volt)
 
    def gen_opc(self):
        """
        Configures the instrument to generate an operation complete message
        by setting bit 0 of the Standard Event Status Register (SESR) when
        all pending commands that generate an OPC message are complete.
        """
        self.inst.write("*OPC")
        
    def get_opc(self):
        """
        Places the ASCII character "1" into the output queue when all such
        OPC commands are complete.
        """
        opc = str(self.inst.query("*OPC?"))
        return(opc)
      
    def set_psc(self, NR1):
        """
        Sets the power-on status flag that controls the automatic
        power-on execution of SRER and ESER. When *PSC is true, the SRER and
        ESER are set to 0 at power-on. When *PSC is false, the current values
        in the SRER and ESER are preserved in nonvolatile memory when power
        is shut off and are restored at power-on.

        Parameters
        ----------
        NR1 : int
            Status of the automatic power-on execution.
        """
        if int(NR1) in range(2):
            self.inst.write(f"*PSC {NR1}")
        else:
            raise ValueError("Value Error. Please input 0 or 1.")
        
    def get_psc(self):
        """
        Returns the power-on status flag that controls the automatic power-on
        execution of SRER and ESER.
        """
        psc = str(self.inst.query*"*PSC?")
        return(psc)
     
    def rcl(self, NR1):
        """
        Restores the state of the power supply from a copy of its settings
        stored in the setup memory. The settings are stored using the *SAV
        command. If the specified setup memory is deleted, this command
        causes an error.

        Parameters
        ----------
        NR1 : int
            Specified memory location.

        Returns
        -------
        None.

        """
        if int(NR1) in range(41):
            self.inst.write(f"*RCL {NR1}")
        else:
            raise ValueError("Value Error. Please input an integer between 0 "
                             "and 40.")
      
    def reset(self):
        """
        Resets the power supply to default settings, but does not purge any
        stored settings.
        """
        self.inst.write("*RST")
        
    def sav(self, NR1):
        """
        Saves the state of the power supply into a specified nonvolatile
        memory location. Any settings that had been stored previously at the
        location are overwritten. You can later use the *RCL command to
        restore the power supply to this saved state.

        Parameters
        ----------
        NR1 : int
            Specified nonvolatile memory location.
        """
        if int(NR1) in range(1, 41):
            self.inst.write(f"*SAV {NR1}")
        else:
            raise ValueError("Value Error. Please eneter an integer between 1"
                              " and 41.")
    
    def set_curr(self, NRf, unit = 'A'):
        """Sets the current value of the power supply in units of A or mA."""
        if unit.upper() == 'MA' and float(NRf): #Converts mA to A
            NRf = float(NRf) / 1000
        if self.get_model() == '2200-72-1' and 0 <= float(NRf) <= 1.2:
            self.inst.write(f"CURR {NRf}A")
        if (self.get_model() in ['2220-30-1', '2220G-30-1'] and
                                0 <= float(NRf) <= 1.5):
            self.inst.write(f"CURR {NRf}A")
        if self.get_model() == '2200-60-2' and 0 <= float(NRf) <= 2.5:
            self.inst.write(f"CURR {NRf}A")
        if (self.get_model() in ['2200-32-3', '2231A-30-3'] and
                                0 <= float(NRf) <= 3):
            self.inst.write(f"CURR {NRf}A")
        if (self.get_model() in ['2200-20-5', '2200-30-5', '2230-30-1',
                                 '2230G-30-1'] and 0 <= float(NRf) <= 5):
            self.inst.write(f"CURR {NRf}A")
        else:
            raise ValueError("Value Error. Please refer to the manual for "
                             "correct parameters.")

    def set_curr_max(self):
        """Sets the currentl value of the power supply to its maximum value."""
        self.inst.write("CURR MAX")
        
    def set_curr_min(self):
        """Sets the currentl value of the power supply to its minimum value."""
        self.inst.write("CURR MIN")
        
    def set_curr_def(self):
        """Sets the currentl value of the power supply to its default value."""
        self.inst.write("CURR DEF")
        
    def get_curr_setting(self):
        """Returns the current value of the power supply."""
        curr_setting = str(self.inst.query("CURR?"))
        return(curr_setting)
     
    def set_ttl(self, NR1):
        """
        Sets the output state of the rear-panel TTL control output the state
        of the rear-panel TTL control input. When the port mode is DIGITAL,
        this command is enabled. 

        Parameters
        ----------
        NR1 : int
            Output state.
        """
        if int(NR1) in range(2):
            self.inst.write(f"DIG:DATA {NR1}")
        else:
            raise ValueError("Value Error. Please enter 0 for low state or 1 "
                             "for high state.")
        
    def get_ttl(self):
        """Returns output state of the rear-panel TTL."""
        ttl = str(self.inst.query("DIG:DATA?"))
        return(ttl)
    
    def set_dig_func(self, string):
        """
        Sets the function of the TTL control lines on the rear panel of the
        power supply.

        Parameters
        ----------
        string : str
            Function of the TTL control.
        """
        if str(string).upper() in ['TRIG', ' TRIGGER', 'RIDFI', 'RIDF', 'DIG',
                                   'DIGITAL']:
            self.inst.write(f"DIGI:FUNC {string}.upper()")
        else:
            raise ValueError("Value Error. Please enter TRIG, RIDF, or DIG.")
  
    def get_dig_func(self):
        """
        Returns the function of the TTL control lines on the rear panel of the
        power supply.
        """
        dig_func = str(self.inst.query("DIGI:FUNC?"))
        return(dig_func)

    def set_func_mode(self, string):
        """
        Can be in either fixed mode or list mode. When this command is in
        fixed mode, the power supply responds to discrete commands. When this
        command is in list mode, the power supply operates in list mode.

        Parameters
        ----------
        string : str
            Mode of the power supply.
        """
        if str(string).upper() in ['FIX', 'FIXED', 'LIST']:
            self.inst.write(f"FUNC:MODE {string}.upper()")
        else:
            raise ValueError("Value Error. Please enter FIX or LIST.")
        
    def get_func_mode(self):
        """Returns mode of the power supply."""
        func_mode = str(self.inst.query("FUNC:MODE?"))
        return(func_mode)
        
    def set_list_count(self, NR1):
        """
        Configures the number of times the active list will execute before
        stopping.

        Parameters
        ----------
        NR1 : int
            Number of times the list will execute before stopping.
        """
        if int(NR1) in range(2, 65536):
            self.inst.write(f"LIST:COUN {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 2 "
                             "and 65535.")
        
    def set_curr_step(self, NR1, NRf, unit = 'A'):
        """
        Sets the current for a list step in units of A or mA.

        Parameters
        ----------
        NR1 : int
            Step number in the active list.
        NRf : float
            Current rating in amperes.
        unit : str, optional
            Unit of current. The default is 'A'.
        """
        if str(unit).upper() == 'MA' and float(NRf):
            NRf = float(NRf) / 1000
        if int(NR1) in range(1, 81):
            if self.get_model() == '2200-72-1' and 0 <= float(NRf) <= 1.2:
                self.inst.write(f"LIST:CURR {NR1}, {NRf}A")
            if (self.get_model() in ['2220-30-1', '2220G-30-1'] and
                                    0 <= float(NRf) <= 1.5):
                self.inst.write(f"LIST:CURR {NR1}, {NRf}A")
            if self.get_model() == '2200-60-2' and 0 <= float(NRf) <= 2.5:
                self.inst.write(f"LIST:CURR {NR1}, {NRf}A")
            if (self.get_model() in ['2200-32-3', '2231A-30-3'] and
                                    0 <= float(NRf) <= 3):
                self.inst.write(f"LIST:CURR {NR1}, {NRf}A")
            if (self.get_model() in ['2200-20-5', '2200-30-5', '2230-30-1',
                                     '2230G-30-1'] and 0 <= float(NRf) <= 5):
                self.inst.write(f"LIST:CURR {NR1}, {NRf}A")
        else:
            raise ValueError("Value Error. Please refer to the manual for "
                             "correct parameters.")
        
    def get_curr_step(self, NR1):
        """
        Returns the current level for a specific step.

        Parameters
        ----------
        NR1 : int
            Step to be selected.
        """
        if int(NR1) in range(1, 81):
            curr_step = str(self.inst.query("LIST:CURR? " + str(NR1)))
            return(curr_step)
        else:
            raise ValueError("Value Error. Please enter an integer between 1 "
                             "and 80.")
        
    def set_list_mode(self, string):
        """
        Determines the response of the power supply to a trigger in listmode.

        Parameters
        ----------
        string : str
            Power supply response.
        """
        if str(string).upper() in ['CONT', 'CONTINUED', 'STEP']:
            self.inst.write("LIST:MODE " + str(string))
        else:
            return("Input error. Please enter CONT or STEP.")
        
    def get_list_mode(self):
        """
        Returns the the response of the power supply to a trigger in listmode.
        """
        list_mode = str(self.inst.query("LIST:MODE?"))
        return(list_mode)
    
    def recall_list(self, NR1):
        """
        Recalls a previously saved list from the specified storage location and
        makes it the active list for editing or execution.

        Parameters
        ----------
        NR1 : int
            Specified storage location.
        """
        if int(NR1) in range(1, 9):
            self.inst.write(f"LIST:RCL {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 1 "
                             "and 8.")
        
    def save_list(self, NR1):
        """
        Saves the active list file to a storage location in nonvolatile
        memory.

        Parameters
        ----------
        NR1 : int
            Storage location.
        """
        if int(NR1) in range(1, 9):
            self.inst.write(f"LIST:SAV {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 1 "
                             "and 8.")
  
    def set_steps(self, NR1):
        """
        Configures the number of steps in the active list. The number of
        steps must be configured before loading the voltage levels, current
        levels, and/or durations of the steps.

        Parameters
        ----------
        NR1 : str, int
            Number of steps in the active list.
        """
        if str(NR1).upper() in ['MIN', 'MAX']:
            self.inst.write(f"LIST:STEP {NR1}.upper()")
        if int(NR1) in range(2, 81):
            self.inst.write(f"LIST:STEP {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 2 "
                             "and 80, or MIN or MAX.")
        
    def set_volt_step(self, NR1, NRf, unit = 'V'):
        """
        Sets the voltage level of a specified step in a list in units of V
        or mV.  

        Parameters
        ----------
        NR1 : int
            Step number in active list.
        NRf : float
            Voltage from the step.
        unit : str, optional
            Unit of voltage. The default is 'V'.
        """
        if str(unit).upper == 'MV' and float(NRf):
            NRf = float(NRf) / 1000
        if int(NR1) in range(1, 81):
            if self.get_model == '2200-20-5' and 0 <= float(NRf) <= 20:
                self.inst.write(f"LIST:VOLT {NR1}, {NRf}V")
            if (self.get_model() in ['2200-30-5', '2230G-30-1', '2230-30-1',
                                    '2220G-30-1', '2220-30-1', '2231A-30-3']
                                    and 0 <= float(NRf) <= 30):
                                        self.inst.write(f"LIST:VOLT {NR1}, "
                                                        "{NRf}V")
            if self.get_model() == '2200-32-3' and 0 <= float(NRf) <= 32:
                self.inst.write(f"LIST:VOLT {NR1}, {NRf}V")
            if self.get_model() == '2200-60-2' and 0 <= float(NRf) <= 60:
                self.inst.write(f"LIST:VOLT {NR1}, {NRf}V")
            if self.get_model() == '2200-72-1' and 0 <= float(NRf) <= 72:
                self.inst.write(f"LIST:VOLT {NR1}, {NRf}V")
        else:
            raise ValueError("Value Error. Please refer to the manual for "
                             "correct parameters.")
        
    def set_step_duration(self, NR1, NRf, unit = 'ms'):
        """
        Sets the duration of a specified step in a list.

        Parameters
        ----------
        NR1 : str, int
            Step in active list.
        NRf : float
            Duration of the step.
        unit : str, optional
            Unit of time. The default is 'ms'.
        """
        if str(unit).lower() == 's' and float(NRf):
            NRf = float(NRf) * 1000
        if str(NR1).upper() in ['MIN', 'MAX'] and 0 <= NRf:
            self.inst.write(f"LIST:WIDTH {NR1}.upper(), {NRf}ms")
        if int(NR1) in range(1, 81) and 0 <= NRf:
            self.inst.write(f"LIST:WIDTH {NR1}, {NRf}ms")
        else:
            return("Input error. Please refer to the manual for correct "
                   "parameters.")

    def set_dfi_output(self, string):
        """
        Associates the DFI TTL output on the rear panel with a specified bit
        in the status byte register (SBR). Once the bit is associated with
        the DFI signal, the DFI signal will reflect the state of the
        specified bit. The port needs to be in the DFI or RI mode before
        using this command.  

        Parameters
        ----------
        string : str
            State of the bit.
        """
        if str(string).upper() in ['OFF', 'QUES', 'OPER', 'ESB', 'RQS']:
            self.inst.write(f"OUT:DFI:SOUR: {string}.upper")
        else:
            raise ValueError("ValueError. Please enter OFF, QUES, OPER, ESB, "
                             "or RQS.")
        
    def get_dfi_output(self):
        """
        Returns the DFI TTl output associated with a specific bit in the
        status byte register (SBR).
        """
        dfi_output = str(self.inst.query("OUT:DFI:SOUR?"))
        return(dfi_output)
    
    def set_pon_state(self, string):
        """
        Configures the power supply to power up with its output turned off,
        or to return the output to the state it was in when it powered down.

        Parameters
        ----------
        string : str
            Configuration of the power supply.
        """
        if str(string).upper() in ['RST', 'RCL0']:
            self.inst.write(f"OUTP:PON {string}.upper()")
        else:
            raise ValueError("Value Error. Please enter RST or RCL0.")
        
    def get_pon_state(self):
        """Returns power on state of the power supply."""
        pon = str(self.inst.query("OUTP:PON?"))
        return(pon)
    
    def clear_trip(self):
        """
        Clears a trip condition caused by over voltage (OV),
        #over temperature(OT), or remote inhibit (RI).
        """
        self.inst.write("OUTP:PROT:CLE")
        
    def set_ri_pin(self, string):
        """
        Sets the input mode of the RI (remote inhibit) input pin.

        Parameters
        ----------
        string : str
            Input mode.
        """
        if str(string).upper() in ['OFF', 'LATC', 'LATCHING', 'LIVE']:
            self.inst.write(f"OUTP:RI:MODE {string}")
        else:
            raise ValueError("Value Error. Please enter OFF, LATC, LATCHING, "
                             "or LIVE.")
        
    def get_ri_pin(self):
        """Returns the input mode of the RI (remote inhibit) input pin."""
        ri = str(self.inst.query("OUTP:RI:MODE?"))
        return(ri)
    
    def set_output_state(self, boolean):
        """
        The power supply output channel on or off.

        Parameters
        ----------
        boolean : str, int
            Output channel status.
        """
        if str(boolean).upper() in ['ON', 'OFF']:
            self.inst.write(f"OUTP {boolean}.upper()")
        if int(boolean) in range(2):
            self.inst.write(f"OUTP {boolean}")
        else:
            raise ValueError("Value Error. Please enter ON, OFF, 0, or 1.")
            
    def get_output_state(self):
        """Returns status of the power supply output."""
        output = str(self.inst.query("OUTP?"))
        return(output)
    
    def set_delay(self, NRf, unit = 'ms'):
        """
        Sets the time duration of the output timer.

        Parameters
        ----------
        NRf : float
            Time duration.
        unit : str, optional
            Unit of time. The default is 'ms'.
        """
        if str(unit).lower() == 'ms' and float(NRf):
            NRf = float(NRf) / 1000
        if str(NRf).upper() in ['MIN', 'MAX', 'DEF']:
            self.inst.write(f"OUTP:TIM:DEL {NRf}.upper()")
        if 0.01 <= float(NRf) <= 60000:
            self.inst.write(f"OUTP:TIM:DEL {NRf}")
        else:
            raise ValueError("Value Error. Please enter a value between 0.01s "
                             "and 60,000s or MIN, MAX, or DEF.")
        
    def get_delay(self):
        """Returns the time duration of the output timer."""
        delay = str(self.inst.query*"OUTP:TIM:DEL?")
        return(delay)
    
    def set_timer(self, boolean):
        """
        Turns the output timer function on and off.

        Parameters
        ----------
        boolean : str, int
            Status of output timer.
        """
        if str(boolean).upper() in ['ON', 'OFF']:
            self.inst.write(f"OUTP:TIM {boolean}.upper()")
        if int(boolean) in range(2):
            self.inst.write(f"OUTP:TIM {boolean}")
        else:
            raise ValueError("Value Error. Please enter ON, OFF, 0, or 1.")
        
    def set_volt(self, NRf, unit = 'V'):
        """
        Sets the voltage value of the power supply.

        Parameters
        ----------
        NRf : str, float
            Voltage value.
        unit : str, optional
            Unit of voltage. The default is 'V'.
        """
        if str(unit).upper() == 'MV' and float(NRf):
            NRf = float(NRf) / 1000
        if str(unit).upper() == 'KV' and float(NRf):
            NRf = float(NRf) * 1000
        
        if str(NRf).upper() in ['MIN', 'MAX', 'DEF']:
            self.inst.write(f"VOLT {NRf}.upper()")
        if 0 <= float(NRf) <= 30:
            self.inst.write(f"VOLT {NRf}")
        else:
            raise ValueError("Value Error. Please enter a value between 0 "
                             "and 30, or MIN, MAX, or DEF.")
            
    def get_voltage(self):
        """Returns the current of the power supply."""
        volt = str(self.inst.query("VOLT?"))
        return(volt)
    
    def set_ovp(self, NRf, unit = 'V'):
        """
        Sets the over voltage protection (OVP) threshold level.

        Parameters
        ----------
        NRf : str, float
            Value of the OVP.
        unit : str, optional
            Unit of voltage. The default is 'V'.
        """
        if str(unit).upper() == 'MV' and float(NRf):
            NRf = NRf / 1000
        if str(NRf).upper() in ['MIN', 'MAX']:
            self.inst.write(f"VOLT:PROT {NRf}")
        if 0 <= float(NRf) <= 30:
            self.inst.write(f"VOLT:PROT {NRf}V")
        else:
            raise ValueError("Value Error. Please enter a value between 0 and"
                             " 30 or MIN or MAX.")
    def get_ovp(self):
        """Returns value of the OVP."""
        ovp = str(self.inst.query("VOLT:PROT?"))
        return(ovp)
    
    def set_ovp_state(self, boolean):
        """
        Activates, deactivates, or checks the status of overvoltage protection.

        Parameters
        ----------
        boolean : str
            State of the OVP.
        """
        if str(boolean).upper() in ['ON', 'OFF']:
            self.inst.write(f"VOLT:PROT:STAT {boolean}.upper()")
        if int(boolean) in range(2):
            self.inst.write(f"VOLT:PROT:STAT {boolean}")
        else:
            raise ValueError("Value Error. Please enter 1, 0, ON, or OFF.")
        
    def get_ovp_state(self):
        """Returns the status of overvoltage protection."""
        ovp_state = str(self.inst.query("VOLT:PROT:STAT?"))
        return(ovp_state)
    
    def volt_range(self, NRf, unit = 'V'):
        """
        Limits the maximum voltage that can be
        programmed on the power supply. This command corresponds to
        the front-panel Max Voltage setting that can be found under the
        Protection submenu. This function is different from OVP, since it
        cannot turn the output off.

        Parameters
        ----------
        NRf : str, float
            Value of max voltage.
        unit : str, optional
            Unit of voltage. The default is 'V'.
        """
        if str(unit).upper() == 'MV' and float(NRf):
            NRf = float(NRf) / 1000
        if str(unit).upper() == 'KV' and float(NRf):
            NRf = float(NRf) * 1000
        if str(NRf).upper() in ['MIN', 'MAX', 'DEF']:
            self.inst.write(f"VOLT:RANG {NRf}.upper()")
        if 0 <= float(NRf) <= 30:
            self.inst.write(f"VOLT:RANG {NRf}V")
        else:
            raise ValueError("Value Error. Please enter a voltage between 0 "
                             "and 30, or MIN, MAX, or DEF.")
        
    def get_volt_range(self):
        """Returns the value of the voltage range."""
        volt_range = str(self.inst.query("VOLT:RANG?"))
        return(volt_range)
    
    def set_sre(self, NR1):
        """
        Sets the bits in the service request enable register (SRER).

        Parameters
        ----------
        NR1 : int
            Bit of the SRER.
        """
        if int(NR1) in range(256):
            self.inst.write(f"*SRE {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 0 "
                             "and 255.")
    def get_sre(self):
        """Returns the bits of the service request enable register (SRER)."""
        sre = str(self.inst.query("*SRE?"))
        return(sre)
    
    def get_ocr(self):
        """Returns the contents of the operation condition register (OCR)."""
        ocr = str(self.inst.query("STAT:OPER:COND?"))
        return(ocr)
    
    def set_oenr(self, NR1):
        """
        Sets  the contents of the operation enable register (OENR). The OENR
        is an eight-bit mask register that determines which bits in the
        Operation Event Register (OEVR) will affect the state of the OPER bit
        in the Status Byte Register (SBR).

        Parameters
        ----------
        NR1 : int
            Contents of OENR.
        """
        if int(NR1) in range(256):
            self.inst.write(f"STAT:OPER:ENAB {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 0 "
                             "and 256.")
    def get_oenr(self):
        """Returns the contents of the operation enable register (OENR)."""
        oenr = str(self.inst.query("STAT:OPER:ENAB?"))
        return(oenr)
    
    def get_oevr(self):
        """
        Returns the contents of the operation event register (OEVR). After
        executing this command the operation event register is reset.
        """
        oevr = str(self.inst.query("STAT:OPER:EVEN?"))
        return(oevr)
    
    def get_qcr(self):
        """Returns the contents of the questionable condition register (QCR)"""
        qcr = str(self.inst.query("STAT:QUEST:COND?"))
        return(qcr)
    
    def set_qenr(self, NR1):
        """
        Sets the contents of the questionable enable register (QENR). The QENR
        is an eight-bit mask register that determines which bits in the
        Questionable Event Register( QEVR) will affect the state of the QUES
        bit in the Status Byte Register (SBR).

        Parameters
        ----------
        NR1 : int
            A decimal integer ranging from 0 through 255. The binary bits 
            of the QENR are set according to this value.
        """
        if int(NR1) in range(256):
            self.inst.write(f"STAT:QUEST:ENAB {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 0 "
                             "and 255")
    def get_qenr(self):
        """Returns the contents of the questionable enable register (QENR)."""
        qenr = str(self.inst.query("STAT:QUEST:ENAB?"))
        return(qenr)
    
    def get_qevr(self):
        """
        Returns the contents of the questionable event register (QEVR). After
        executing this command, the quest event register is reset.
        """
        qevr = str(self.inst.query("STAT:QUES?"))
        return(qevr)
    
    def set_ntr(self, NR1):
        """
        Sets the negative transition filter of the questionable event register.
        The filter contents cause the corresponding bit in the questionable
        event register to become 1 when the bit value of the questionable
        condition register transitions from 1 to 0.

        Parameters
        ----------
        NR1 : int
             A number ranging from 0 through 255. The binary bits of the
             Questionable NTR register are set according to this value.
        """
        if int(NR1) in range(256):
            self.inst.write(f"STAT:QUES:NTR {NR1}")
        else:
            raise ValueError("ValueError. Please enter an integer between 0 "
                             "and 255.")
            
    def get_ntr(self):
        """
        Returns the value of the negative transition filter of the questionable
        event register.
        """
        ntr = str(self.inst.query("STAT:QUES:NTR?"))
        return(ntr)
    
    def set_ptr(self, NR1):
        """
        Sets the positive transition filter of the questionable event register.
        The filter contents cause the corresponding bit in the questionable
        event register to become 1 when the bit value of the questionable
        condition register transitions from 0 to 1.

        Parameters
        ----------
        NR1 : TYPE
             A number ranging from 0 through 255. The binary bits the
             questionable PTR register are set according to this value.
        """
        if int(NR1) in range(256):
            self.inst.write(f"STAT:QUES:PTR {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 0 "
                             "and 255.")
    
    def get_ptr(self):
        """
        Returns the positive transition filter of the questionable event
        register.
        """
        ptr= str(self.inst.query("STAT:QUES:PTR?"))
        return(ptr)
    
    def get_sbr(self):
        """
        Returns the contents of the status byte register (SBR) using the Master
        Summary Status (MSS) bit.
        """
        sbr = str(self.inst.query("*SRE?"))
        return(sbr)
    
    def get_error(self):
        """
        Queries the error code and error information of the power supply and
        returns both values.
        """
        error = str(self.inst.query("SYST:ERR?"))
        return(error)
    
    def key(self, NR1):
        """
        This command can produce the same effect as pressing one of the
        front-panel buttons. The instrument must be in local mode in order for
        fthis command to simulate a front-panel button press.

        Parameters
        ----------
        NR1 : int
            Integer key code.
        """
        if int(NR1) in range(1, 23) or int(NR1) == 64:
            self.inst.write(f"SYST:KEY {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 1 "
                             "and 22,or 64.")
            
    def syst_local(self):
        """Sets the power supply for control from the frontpanel."""
        self.inst.write("SYS:LOC")
        
    def syst_pos(self, string):
        """
         Determines how the power supply initializes when its power switch is
         turned on. This command configures the instrument to power up with
         default settings, or power up with the settings that were in effect
         when the instrument was turned off.

        Parameters
        ----------
        string : str
            Initialization of the power setting.
        """
        if str(string).upper() in ['RST', 'RCL0']:
            self.inst.write(f"SYST:POS {string}.upper()")
        else:
            raise ValueError("Value Error. Please enter either RST or RCL0.")
    
    def get_syst_pos(self):
        """Returns the initilization setting of the power supply."""
        pos = str(self.inst.query("SYST:POS?"))
        return(pos)
    
    def syst_remote(self):
        """Sets the power supply to remote control mode."""
        self.inst.write("SYST:REM")
        
    def syst_lock(self):
        """
        If the power supply is in remote mode, this command locks out the
        front panel LOCAL button. This command has no effect if the
        instrument is in local mode.
        """
        self.inst.write("SYST:RWL")
        
    def get_syst_version(self):
        """Returns SCPI version of the instrument."""
        scpi = str(self.inst.query("SYST:VER?"))
        return(scpi)
    
    def trigger(self):
        """Generates a trigger event."""
        self.inst.write("*TRG")
        
    def force_trigger(self):
        """Forces an immediate trigger event."""
        self.inst.write("TRIG")
        
    def trigger_source(self, string):
        """
        Sets the source of trigger events.

        Parameters
        ----------
        string : str
            Source of trigger event.
        """
        if str(string).upper() in ['MAN', 'IMM', 'EXT', 'BUS']:
            self.inst.write(f"TRIG:SOUR {string}.upper()")
        else:
            raise ValueError("Value Error. Please enter MAN, IMM, EXT, or BUS")
            
    def get_trigger_source(self):
        """Returns the source of the trigger event."""
        trig_event = str(self.inst.query("TRIG:SOUR?"))
        return(trig_event)
    
    def get_test(self):
        """Initiates a self-test and reports any errors."""
        test = str(self.inst.query("*TST?"))
        return(test)
    
    def wait(self):
        """
        Prevents the instrument from executing further
        commands or queries until all pending commands are complete.
        """
        self.inst.write("*WAI")