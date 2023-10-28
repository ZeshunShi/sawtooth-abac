echo "Running experiment for PoET"
echo "Batch: 10"
node run-benchmark.js -c ../benchmark/abac/Caliper/ABAC_worker1_batch10.yaml -n ../network/sawtooth/sawtooth-poet-5nodes/sawtooth.json
sleep 5
node run-benchmark.js -c ../benchmark/abac/Caliper/ABAC_worker5_batch10.yaml -n ../network/sawtooth/sawtooth-poet-5nodes/sawtooth.json
sleep 5
node run-benchmark.js -c ../benchmark/abac/Caliper/ABAC_worker10_batch10.yaml -n ../network/sawtooth/sawtooth-poet-5nodes/sawtooth.json
sleep 5
echo "Batch: 100"
node run-benchmark.js -c ../benchmark/abac/Caliper/ABAC_worker1_batch100.yaml -n ../network/sawtooth/sawtooth-poet-5nodes/sawtooth.json
sleep 5
node run-benchmark.js -c ../benchmark/abac/Caliper/ABAC_worker5_batch100.yaml -n ../network/sawtooth/sawtooth-poet-5nodes/sawtooth.json
sleep 5
node run-benchmark.js -c ../benchmark/abac/Caliper/ABAC_worker10_batch100.yaml -n ../network/sawtooth/sawtooth-poet-5nodes/sawtooth.json
sleep 5


echo "Running experiment for PBFT"
echo "Batch: 10"
node run-benchmark.js -c ../benchmark/abac/Caliper/ABAC_worker1_batch10.yaml -n ../network/sawtooth/sawtooth-pbft-5nodes/sawtooth.json
sleep 5
node run-benchmark.js -c ../benchmark/abac/Caliper/ABAC_worker5_batch10.yaml -n ../network/sawtooth/sawtooth-pbft-5nodes/sawtooth.json
sleep 5
node run-benchmark.js -c ../benchmark/abac/Caliper/ABAC_worker10_batch10.yaml -n ../network/sawtooth/sawtooth-pbft-5nodes/sawtooth.json
sleep 5
echo "Batch: 100"
node run-benchmark.js -c ../benchmark/abac/Caliper/ABAC_worker1_batch100.yaml -n ../network/sawtooth/sawtooth-pbft-5nodes/sawtooth.json
sleep 5
node run-benchmark.js -c ../benchmark/abac/Caliper/ABAC_worker5_batch100.yaml -n ../network/sawtooth/sawtooth-pbft-5nodes/sawtooth.json
sleep 5
node run-benchmark.js -c ../benchmark/abac/Caliper/ABAC_worker10_batch100.yaml -n ../network/sawtooth/sawtooth-pbft-5nodes/sawtooth.json
sleep 5


echo "Running experiment for Raft"
echo "Batch: 10"
node run-benchmark.js -c ../benchmark/abac/Caliper/ABAC_worker1_batch10.yaml -n ../network/sawtooth/sawtooth-raft-5nodes/sawtooth.json
sleep 5
node run-benchmark.js -c ../benchmark/abac/Caliper/ABAC_worker5_batch10.yaml -n ../network/sawtooth/sawtooth-raft-5nodes/sawtooth.json
sleep 5
node run-benchmark.js -c ../benchmark/abac/Caliper/ABAC_worker10_batch10.yaml -n ../network/sawtooth/sawtooth-raft-5nodes/sawtooth.json
sleep 5
echo "Batch: 100"
node run-benchmark.js -c ../benchmark/abac/Caliper/ABAC_worker1_batch100.yaml -n ../network/sawtooth/sawtooth-raft-5nodes/sawtooth.json
sleep 5
node run-benchmark.js -c ../benchmark/abac/Caliper/ABAC_worker5_batch100.yaml -n ../network/sawtooth/sawtooth-raft-5nodes/sawtooth.json
sleep 5
node run-benchmark.js -c ../benchmark/abac/Caliper/ABAC_worker10_batch100.yaml -n ../network/sawtooth/sawtooth-raft-5nodes/sawtooth.json
sleep 5