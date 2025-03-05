export function formatToShortDate(dateString) {
    const date = new Date(dateString);
  
    if (isNaN(date)) return "Invalid Date";
  
    return date.toLocaleDateString("en-US", { 
      year: "numeric", 
      month: "short",  // "Feb"
      day: "numeric"   // "1"
    });
  }