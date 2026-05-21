using ImmiAccount.Data;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace ImmiAccount.Pages.Applications;

public class IndexModel : PageModelBase
{
    private readonly AppDbContext _db;

    public IndexModel(AppDbContext db) => _db = db;

    public record AppSummary(
        string Id, string DisplayName, string DateOfBirth,
        string SubclassName, string CurrentStatus, string ReferenceNumber,
        string LastUpdated, string DateLodged);

    public List<AppSummary> Applications { get; set; } = new();

    public IActionResult OnGet()
    {
        var redirect = CheckAuth();
        if (redirect != null) return redirect;

        Applications = _db.Applications
            .Include(a => a.Subclass)
            .Include(a => a.Applicant)
            .Where(a => a.ApplicantId == CurrentUserId!.Value)
            .OrderByDescending(a => a.LastUpdated)
            .Select(a => new AppSummary(
                a.Id,
                a.Applicant!.DisplayName,
                a.Applicant.DateOfBirth,
                a.Subclass!.Name,
                a.CurrentStatus,
                a.ReferenceNumber,
                a.LastUpdated,
                a.DateLodged))
            .ToList();

        return Page();
    }
}
