document.addEventListener("DOMContentLoaded", function () {
var leftList = document.getElementById("left-list");
var rightSlots = document.querySelectorAll(".sortable-slot");
var submitBtn = document.getElementById("submit-btn");

const FieldName = js_vars.field_name;
var hiddenInput = document.getElementById(FieldName);

console.log('field name',FieldName);



// Initialize sortable for left list (unranked items)
new Sortable(leftList, {
    group: "shared",
    animation: 150,
});

// Initialize sortable for each ranking slot (only one item per slot)
rightSlots.forEach(slot => {
  new Sortable(slot, {
    group: "shared",
    animation: 150,
    swapThreshold: 1,
    onAdd(evt) {
      const incoming = evt.item;                  // the element just dropped in
      const itemsInSlot = slot.querySelectorAll('.sortable-item');

      // Remove placeholder if it’s still there
      const placeholder = slot.querySelector('.placeholder');
      if (placeholder) placeholder.remove();

      // If there was already an item here, it will now be in itemsInSlot too.
      // Find the one that *isn't* the incoming element, and send it back.
      if (itemsInSlot.length > 1) {
        const toReturn = Array.from(itemsInSlot).find(el => el !== incoming);
        leftList.appendChild(toReturn);
      }

      updateRankingOrder();
    },
    onRemove(evt) {
      // If that drop left the slot empty, re-add the placeholder
      if (!slot.querySelector('.sortable-item')) {
        const placeholderSpan = document.createElement("span");
        placeholderSpan.classList.add("placeholder");
        placeholderSpan.textContent = "[Drag & Drop here]";
        slot.appendChild(placeholderSpan);
      }
      updateRankingOrder();
    }
  });
});


function updateRankingOrder() {
    var order = [];
    rightSlots.forEach(slot => {
        let item = slot.querySelector(".sortable-item");
        order.push(item ? item.dataset.value : null);
    });

    hiddenInput.value = JSON.stringify(order);

    // Enable submit button only if all slots are filled
    submitBtn.disabled = order.includes(null);

    // console.log("🔥 Current ranking order:", order);
}

submitBtn.addEventListener("click", function () {
    updateRankingOrder();
    document.forms[0].submit();
});
});