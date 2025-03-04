import React from "react";

function TeamStatusChip({ status }) {
  const statusStyles = {
    active: {
      background: "linear-gradient(to right, #4CAF50, #66BB6A)",
      color: "white",
      border: "1px solid #388E3C",
    },
    suspended: {
      background: "linear-gradient(to right, #E53935, #EF5350)",
      color: "white",
      border: "1px solid #B71C1C",
    },
    default: {
      background: "linear-gradient(to right, #9E9E9E, #BDBDBD)",
      color: "white",
      border: "1px solid #616161",
    },
  };

  const style = statusStyles[status.toLowerCase()] || statusStyles.default;

  return (
    <span
      style={{
        ...style,
        padding: "6px 14px",
        borderRadius: "20px",
        fontWeight: "600",
        fontSize: "0.9rem",
        display: "inline-flex",
        justifyContent: "center",
        alignItems: "center",
        minWidth: "120px", // Ensures uniform width
        textAlign: "center",
        boxShadow: "0 2px 4px rgba(0, 0, 0, 0.2)",
      }}
    >
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  );
}

export default TeamStatusChip;
