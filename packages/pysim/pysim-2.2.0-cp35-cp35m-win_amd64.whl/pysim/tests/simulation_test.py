﻿"""Tests various aspects of the Sim object that is not tested in other
places
"""
import tempfile
import json
import numpy as np
import pytest

from pysim.simulation import Sim
from pysim.systems import VanDerPol
from pysim.systems import MassSpringDamper
from pysim.systems import DiscretePID
from pysim.systems import RigidBody
from pysim.systems import LogisticMap
from pysim.systems.python_systems import VanDerPol as PyVanDerPol

__copyright__ = 'Copyright (c) 2014-2016 SSPA Sweden AB'

@pytest.mark.parametrize("test_class",[VanDerPol,PyVanDerPol])
def test_gettime(test_class):
    """Test that the elapsed time is returned from the simulation"""
    sys = test_class()
    sim = Sim()
    sim.add_system(sys)
    integrationlength = 2.0
    assert sim.get_time() == 0.0
    sim.simulate(integrationlength, 0.1)
    assert sim.get_time() == integrationlength

@pytest.mark.parametrize("test_class",[VanDerPol,PyVanDerPol])
def test_store_config(test_class):
    """Test that it is possible to store the simulation to a file.
    In this test a temp file is used, it should be deleted automatically
    after the test.
    """
    sys = test_class()
    sim = Sim()
    sim.add_system(sys)
    sys.inputs.a = 1.234
    sys.store("x")

    file = tempfile.NamedTemporaryFile(delete=False)
    file.close()
    sim.save_config(file.name)

    file2 = open(file.name)
    simdict = json.load(file2)
    file2.close()
    assert simdict["systems"]["vanderpol"]["inputs"]["a"] == 1.234
    assert "x" in simdict["systems"]["vanderpol"]["stores"]

def test_load_config():
    """Tests the loading of a system configuration from file"""

    configstring = """{
    "systems": {
        "vanderpol1": {
            "inputs": {
                "a": 1.234,
                "b": 1.0
            },
            "module": "pysim.systems",
            "type": "VanDerPol"
        },
       "vanderpol2": {
            "inputs": {
                "a": 1.0,
                "b": 3.456
            },
            "module": "pysim.systems.python_systems",
            "type": "VanDerPol"
        }
    }
}
"""

    sim = Sim()
    file = tempfile.NamedTemporaryFile(delete=False, mode="w+")
    file.write(configstring)
    file.close()
    sim.load_config(file.name)
    assert sim.systems["vanderpol1"].inputs.a == 1.234
    assert sim.systems["vanderpol2"].inputs.b == 3.456

def test_connected_system():
    """Check that the time for stored values in a discrete system is
    regurarly spaced"""

    #Create Simulaton
    sim = Sim()

    #Create, setup and add system to simulation
    sys = MassSpringDamper()
    sys.store("x1")
    sys.inputs.b = 50
    sys.inputs.f = 0
    sim.add_system(sys)

    controlsys = DiscretePID()
    controlsys.inputs.refsig = 1.0
    controlsys.inputs.p = 1
    controlsys.inputs.plim = 400.0
    controlsys.inputs.i = 0
    controlsys.inputs.stepsize = 0.3
    controlsys.store("outsig")
    sim.add_system(controlsys)

    sys.connections.add_connection("x1", controlsys, "insig")
    sys.connections.add_connection("x2", controlsys, "dsig")
    controlsys.connections.add_connection("outsig", sys, "f")
    controlsys.inputs.d = 1

    sim.simulate(5, 0.1)

    assert np.max(np.abs(np.diff(controlsys.res.time))-0.1) < 1e-14
    assert np.max(np.abs(np.diff(sys.res.time))-0.1) < 1e-14

def test_multiple_simulationobject():
    """Tests that it is possible to run multiple instances of the Sim object
    and that the results stay the same."""
    sim = Sim()
    sys = MassSpringDamper()
    sys.store("x1")
    sys.inputs.b = 50
    sys.inputs.f = 0
    sim.add_system(sys)
    sim.simulate(5, 0.1)
    xref = sys.res.x1
    for dummy in range(60):
        #Create Simulaton
        sim = Sim()
        sys = MassSpringDamper()
        sys.store("x1")
        sys.inputs.b = 50
        sys.inputs.f = 0
        sim.add_system(sys)
        sim.simulate(5, 0.1)
        x = sys.res.x1
        assert np.all(xref == x)

def test_state_break_larger():
    """Stop the simulation once the value of a state is 
    larger than a preset value
    """
    sim = Sim()
    sys = VanDerPol()
    sys.add_break_greater("y",1.0)
    sim.add_system(sys)
    sim.simulate(20,0.01)

    #If correct the simulation should break at time 0.79
    assert sys.res.time[-1] == 0.79

def test_state_break_smaller():
    """Stop the simulation once the value of a state is 
    larger than a preset value
    """
    sim = Sim()
    sys = VanDerPol()
    sys.add_break_smaller("x",-1.0)
    sim.add_system(sys)
    sim.simulate(20,0.01)

    #If correct the simulation should break at time 2.52
    assert sys.res.time[-1] == 2.52

def test_boost_vector_states():
    """Perform a basic simulation of a system with boost vector states"""
    sim = Sim()
    sys = RigidBody()

    sys.store("position")

    sys.inputs.force =  [1.0,0.0,0.0]
    sys.inputs.mass = 1.0

    sim.add_system(sys)
    sim.simulate(20,0.01)

    pos = sys.res.position
    diff = np.abs(pos[-1,:]-[200,0,0])
    assert np.max(diff) <= 1

def test_discrete_system():
    """Test a discrete system to make sure the results
    are correct. The system tested is a logistical map
    system and it is compared to a function created in 
    this test which also gives the solution.
    """
    lm = LogisticMap()
    lm.inputs.r = 3.6
    lm.states.x = 0.5
    lm.store("x")
    sim = Sim()
    sim.add_system(lm)

    sim.simulate(10,0.1)
    x = [0.5]
    r = 3.6
    for dummy in range(9):
        x.append(r*x[-1]*(1-x[-1]))

    assert np.all(np.abs(lm.res.x[1::10]-x)<1e-18)



if __name__ == "__main__":
    test_store_config(VanDerPol)
