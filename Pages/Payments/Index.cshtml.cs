using ImmiAccount.Data;
using ImmiAccount.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace ImmiAccount.Pages.Payments;

public class IndexModel : PageModelBase
{
    private readonly AppDbContext _db;

    public IndexModel(AppDbContext db) => _db = db;

    public List<Payment> Payments { get; set; } = new();
    public string DisplayName { get; set; } = "";

    public IActionResult OnGet()
    {
        var redirect = CheckAuth();
        if (redirect != null) return redirect;

        var user = _db.Users.Find(CurrentUserId!.Value);
        DisplayName = user?.DisplayName ?? "";

        Payments = _db.Payments
            .Include(p => p.Application)
            .Where(p => p.Application != null && p.Application.ApplicantId == CurrentUserId!.Value)
            .ToList();

        return Page();
    }
}
