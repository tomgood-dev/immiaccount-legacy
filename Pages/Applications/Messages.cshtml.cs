using ImmiAccount.Data;
using ImmiAccount.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace ImmiAccount.Pages.Applications;

public class MessagesModel : PageModelBase
{
    private readonly AppDbContext _db;

    public MessagesModel(AppDbContext db) => _db = db;

    public List<Correspondence> Correspondence { get; set; } = new();
    public string AgentEmail { get; set; } = "";

    public IActionResult OnGet(string appId)
    {
        var redirect = CheckAuth();
        if (redirect != null) return redirect;

        var application = _db.Applications
            .Include(a => a.Subclass)
            .Include(a => a.Applicant)
            .FirstOrDefault(a => a.Id == appId && a.ApplicantId == CurrentUserId!.Value);

        if (application == null) return RedirectToPage("/Applications/Index");

        AgentEmail = application.Applicant?.AgentEmail ?? "";

        Correspondence = _db.Correspondence
            .Where(c => c.ApplicationId == appId)
            .OrderBy(c => c.DateSent)
            .ToList();

        ViewData["AppId"] = appId;
        ViewData["ActiveTab"] = "messages";
        ViewData["AppReference"] = application.ReferenceNumber;
        ViewData["AppSubclassName"] = application.Subclass!.Name;
        ViewData["Title"] = $"Messages - {application.ReferenceNumber}";
        return Page();
    }
}
