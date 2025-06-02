function calculateTonnage(input) {
  if (!input) return 0;

  const sets = input.split(",").map(s => s.trim());
  let total = 0;

  for (let set of sets) {
    //replace "lbs" with "лбс" for consistency
    set = set.replace(/lbs/i, "лбс");
    // Пример: "115лбс 15-14-14"
    const match = set.match(/(\d+)\s*лбс\s*(\d+(?:-\d+)*)/i);
    if (match) {
      const weight = parseFloat(match[1]);
      const reps = match[2].split("-").map(Number).reduce((a, b) => a + b, 0);
      total += weight * reps;
    }
  }

  return total === 0 ? "" : total;
}

function calculateAverageWeightPerRep(input) {
  if (!input) return 0;

  const sets = input.split(",").map(s => s.trim());
  let totalWeight = 0;
  let totalReps = 0;

  for (let set of sets) {
    //replace "lbs" with "лбс" for consistency
    set = set.replace(/lbs/i, "лбс");
    const match = set.match(/(\d+)\s*лбс\s*(\d+(?:-\d+)*)/i);
    if (match) {
      const weight = parseFloat(match[1]);
      const repsList = match[2].split("-").map(Number);
      const reps = repsList.reduce((a, b) => a + b, 0);
      totalWeight += weight * reps;
      totalReps += repsList.length;
    }
  }

  return totalReps > 0 ? totalWeight / totalReps : 0;
}

function calculateMaxWeightTimesBestSet(input) {
  if (!input) return 0;

  const sets = input.split(",").map(s => s.trim());
  let maxWeight = 0;
  let maxRepsAtMaxWeight = 0;

  for (let set of sets) {
    //replace "lbs" with "лбс" for consistency
    set = set.replace(/lbs/i, "лбс");
    const match = set.match(/(\d+)\s*лбс\s*(\d+(?:-\d+)*)/i);
    if (match) {
      const weight = parseFloat(match[1]);
      const repsList = match[2].split("-").map(Number);
      const maxRepsInSet = Math.max(...repsList);

      if (weight > maxWeight) {
        maxWeight = weight;
        maxRepsAtMaxWeight = maxRepsInSet;
      } else if (weight === maxWeight && maxRepsInSet > maxRepsAtMaxWeight) {
        maxRepsAtMaxWeight = maxRepsInSet;
      }
    }
  }

  return maxWeight * maxRepsAtMaxWeight;
}
