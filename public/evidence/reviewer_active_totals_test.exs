defmodule GroupStayWeb.ReviewerActiveTotalsTest do
  use GroupStayWeb.ConnCase
  import GroupStayWeb.PartnerCase

  test "group totals become zero when its last active room is cancelled", %{conn: conn} do
    submit(conn, [open_group_op(), payment_op()])
    submit_one(conn, cancel_rooms_op(%{occurred_on: "2026-11-26"}))
    before_last = read_group(conn, "group-81")
    submit_one(conn, cancel_rooms_op(%{
      operation_id: "op-cancel-last",
      occurred_on: "2026-11-26",
      room_ids: ["room-b"]
    }))
    after_last = read_group(conn, "group-81")
    fields = ~w(status lodging_total_cents deposit_due_cents deposit_paid_cents cash_paid_cents credit_paid_cents outstanding_deposit_cents)
    IO.puts("REVIEW_EVIDENCE " <> Jason.encode!(%{
      before_last: Map.take(before_last, fields),
      after_last: Map.take(after_last, fields),
      active_rooms: Enum.count(after_last["rooms"], &(&1["status"] == "active")),
      ledger: read_ledger(conn)
    }))
    assert after_last["status"] == "cancelled"
    assert Enum.all?(after_last["rooms"], &(&1["status"] == "cancelled"))
    assert Map.take(after_last, tl(fields)) == Map.new(tl(fields), &{&1, 0})
  end
end
