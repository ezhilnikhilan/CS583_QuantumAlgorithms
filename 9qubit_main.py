import random
import cirq

class OneQubitShorsCode:
    def __init__(self):
        self.num_physical_qubits = 9
        self.physical_qubits = cirq.LineQubit.range(self.num_physical_qubits)

    def encode(self):
        yield cirq.Moment([cirq.CNOT(self.physical_qubits[0], self.physical_qubits[3])])
        yield cirq.Moment([cirq.CNOT(self.physical_qubits[0], self.physical_qubits[6])])
        yield cirq.Moment(
            [
                cirq.H(self.physical_qubits[0]),
                cirq.H(self.physical_qubits[3]),
                cirq.H(self.physical_qubits[6]),
            ]
        )
        yield cirq.Moment(
            [
                cirq.CNOT(self.physical_qubits[0], self.physical_qubits[1]),
                cirq.CNOT(self.physical_qubits[3], self.physical_qubits[4]),
                cirq.CNOT(self.physical_qubits[6], self.physical_qubits[7]),
            ]
        )
        yield cirq.Moment(
            [
                cirq.CNOT(self.physical_qubits[0], self.physical_qubits[2]),
                cirq.CNOT(self.physical_qubits[3], self.physical_qubits[5]),
                cirq.CNOT(self.physical_qubits[6], self.physical_qubits[8]),
            ]
        )

    def apply_gate(self, gate: cirq.Gate, pos: int):
        if pos > self.num_physical_qubits:
            raise IndexError
        else:
            return gate(self.physical_qubits[pos])

    def correct(self):
        yield cirq.Moment(
            [
                cirq.CNOT(self.physical_qubits[0], self.physical_qubits[1]),
                cirq.CNOT(self.physical_qubits[3], self.physical_qubits[4]),
                cirq.CNOT(self.physical_qubits[6], self.physical_qubits[7]),
            ]
        )
        yield cirq.Moment(
            [
                cirq.CNOT(self.physical_qubits[0], self.physical_qubits[2]),
                cirq.CNOT(self.physical_qubits[3], self.physical_qubits[5]),
                cirq.CNOT(self.physical_qubits[6], self.physical_qubits[8]),
            ]
        )
        yield cirq.Moment(
            [
                cirq.CCNOT(
                    self.physical_qubits[1], self.physical_qubits[2], self.physical_qubits[0]
                ),
                cirq.CCNOT(
                    self.physical_qubits[4], self.physical_qubits[5], self.physical_qubits[3]
                ),
                cirq.CCNOT(
                    self.physical_qubits[7], self.physical_qubits[8], self.physical_qubits[6]
                ),
            ]
        )
        yield cirq.Moment(
            [
                cirq.H(self.physical_qubits[0]),
                cirq.H(self.physical_qubits[3]),
                cirq.H(self.physical_qubits[6]),
            ]
        )
        yield cirq.Moment([cirq.CNOT(self.physical_qubits[0], self.physical_qubits[3])])
        yield cirq.Moment([cirq.CNOT(self.physical_qubits[0], self.physical_qubits[6])])
        yield cirq.Moment(
            [cirq.CCNOT(self.physical_qubits[3], self.physical_qubits[6], self.physical_qubits[0])]
        )

def comp_round(num, decs = 2):
   return round(num.real, decs) + round(num.imag, decs) * 1j

def construct_circuit(code, errors):
    #Set up the initial state
    circuit = cirq.Circuit([code.apply_gate(cirq.T ** random.random(), 0), code.apply_gate(cirq.X ** random.random(), 0), code.apply_gate(cirq.Y ** random.random(), 0), code.apply_gate(cirq.Z ** random.random(), 0)])
    
    fs =circuit.final_state_vector(initial_state=0)
    fsn = len(fs)
    initial_amps = (comp_round(sum(fs[:fsn//2]),2), comp_round(sum(fs[fsn//2:]),2))
    
    #Encoding
    circuit += cirq.Circuit(code.encode())

    # create error
    '''circuit += cirq.Circuit([
        code.apply_gate(cirq.X,random.randint(0, code.num_physical_qubits - 1)),
        code.apply_gate(cirq.X,random.randint(0, code.num_physical_qubits - 1)),
        code.apply_gate(cirq.X,0)
    ])
    circuit += cirq.Circuit(
        code.apply_gate(cirq.Z, random.randint(0, code.num_physical_qubits - 1)),
        code.apply_gate(cirq.Z, random.randint(0, code.num_physical_qubits - 1)),
        code.apply_gate(cirq.Z, 0)
    )'''
    for gates, qubit in errors:
        for gate in gates:
            circuit += cirq.Circuit(code.apply_gate(gate, qubit))

    # correct error and decode
    circuit += cirq.Circuit(code.correct())
    fs =circuit.final_state_vector(initial_state=0)
    fsn = len(fs)
    final_amps = (comp_round(sum(fs[:fsn//2]),2), comp_round(sum(fs[fsn//2:]),2))

    return initial_amps, final_amps, (initial_amps == final_amps or initial_amps == (-final_amps[0], -final_amps[1])), circuit


if __name__ == '__main__':
    # coverage: ignore

    # create circuit with 9 physical qubits
    code = OneQubitShorsCode()
    error_gates = [[cirq.X],[cirq.Z], [cirq.Z, cirq.X]]
    correction_percentage = {}
    uncorrected_qubits_dict = {i:0 for i in range(9)}
    iterations = 1000
    error_count = 5
    for p in range(0,325,25):
        successful_corrections = 0
        #uncorrected_qubits = []
        for _ in range(iterations):
            errors = []
            error_qubits = []

            for i in random.sample(list(range(9)), error_count): #range(error_count):
                #error_qubits.append(random.randint(0, code.num_physical_qubits - 1))
                gen = random.randint(0,1000)
                if gen < p:
                    error_qubits.append(i)
                    errors.append((error_gates[random.randint(0,2)], error_qubits[-1]))
            #errors = [(error_gates[random.randint(0,2)], random.randint(0, code.num_physical_qubits - 1)), (error_gates[random.randint(0,2)], random.randint(0, code.num_physical_qubits - 1))]
            ia, fa, corrected, circuit = construct_circuit(code, errors)
            successful_corrections += corrected

            '''if not corrected:
                for eq in error_qubits:
                    uncorrected_qubits_dict[eq] += 1
                #uncorrected_qubits.append(tuple(sorted(error_qubits)))
                #print(ia, cirq.dirac_notation(circuit.final_state_vector(initial_state=0)))'''

        
        correction_percentage[p/1000] = (successful_corrections/iterations)*100
        #uncorrected_qubits_dict[error_count] = uncorrected_qubits

        print(f'For error count {error_count}, and probability {p/1000} {(successful_corrections/iterations)*100} % of errors are recovered')

    '''file1 = open("correction_percentage_unrepeated.txt", "a") 
    file1.write(str(correction_percentage))
    file1.close() 
    file2 = open("uncorrected_qubits_count.txt", "a") 
    file2.write(str(uncorrected_qubits_dict))
    file2.close() '''
    file1 = open("prob_error_correction.txt", "a") 
    file1.write(str(correction_percentage))
    file1.close() 