from flask import Flask, render_template, request
import quantum_utils as qu

app = Flask(__name__)

def calculate_accuracy(original, decrypted):
    # Count the number of matching characters between the original and decrypted messages
    matches = sum(o == d for o, d in zip(original, decrypted))
    # Calculate the accuracy percentage
    accuracy = (matches / len(original)) * 100 if original else 0
    return round(accuracy, 2)  # Round to two decimal places for display

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/encrypt/', methods=['GET', 'POST'])
def encrypt():
    if request.method == 'POST':
        message = request.form['message']
        
        # BB84 Protocol Steps
        secret_key = qu.generate_secret_key()
        sender_circuit, sender_qreg, sender_creg = qu.create_sender_circuit(secret_key)
        polarization_table = qu.apply_polarization(sender_circuit, sender_qreg)
        receiver_circuit, receiver_qreg, receiver_creg = qu.send_quantum_state(sender_circuit)
        filtration_table = qu.measure_receiver_state(receiver_circuit, receiver_qreg)
        measured_values = qu.execute_quantum_circuit(receiver_circuit)
        final_key = qu.extract_final_secret_key(polarization_table, filtration_table, measured_values)
        ciphered_message = qu.cipher_message(message, final_key)
        decrypted_message = qu.decipher_message(ciphered_message, final_key)

        # Calculate accuracy
        accuracy = calculate_accuracy(message, decrypted_message)

        # Pass all variables to the encrypt_result.html template
        return render_template('encrypt_result.html', 
                               original_message=message, 
                               ciphered_message=ciphered_message, 
                               decrypted_message=decrypted_message,
                               secret_key=secret_key,
                               polarization_table=polarization_table,
                               filtration_table=filtration_table,
                               measured_values=measured_values,
                               final_key=final_key,
                               accuracy=accuracy)
    return render_template('encrypt.html')

@app.route('/decrypt/', methods=['GET', 'POST'])
def decrypt():
    if request.method == 'POST':
        message = request.form['message']
        
        # BB84 Protocol Steps
        secret_key = qu.generate_secret_key()
        sender_circuit, sender_qreg, sender_creg = qu.create_sender_circuit(secret_key)
        polarization_table = qu.apply_polarization(sender_circuit, sender_qreg)
        receiver_circuit, receiver_qreg, receiver_creg = qu.send_quantum_state(sender_circuit)
        filtration_table = qu.measure_receiver_state(receiver_circuit, receiver_qreg)
        measured_values = qu.execute_quantum_circuit(receiver_circuit)
        final_key = qu.extract_final_secret_key(polarization_table, filtration_table, measured_values)
        decrypted_message = qu.decipher_message(message, final_key)
        ciphered_message = qu.cipher_message(decrypted_message, final_key)

        # Calculate accuracy
        accuracy = calculate_accuracy(message, decrypted_message)

        # Pass all variables to the decrypt_result.html template
        return render_template('decrypt_result.html', 
                               original_message=message, 
                               ciphered_message=ciphered_message, 
                               decrypted_message=decrypted_message,
                               secret_key=secret_key,
                               polarization_table=polarization_table,
                               filtration_table=filtration_table,
                               measured_values=measured_values,
                               final_key=final_key,
                               accuracy=accuracy)
    return render_template('decrypt.html')

if __name__ == '__main__':
    app.run(debug=True)
