using ImmiAccount.Data;
using ImmiAccount.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace ImmiAccount.Pages.Applications;

public class DetailModel : PageModelBase
{
    private readonly AppDbContext _db;

    public DetailModel(AppDbContext db) => _db = db;

    public VisaApplication? Application { get; set; }

    public IActionResult OnGet(string appId)
    {
        var redirect = CheckAuth();
        if (redirect != null) return redirect;

        Application = _db.Applications
            .Include(a => a.Subclass)
            .Include(a => a.Applicant)
            .FirstOrDefault(a => a.Id == appId && a.ApplicantId == CurrentUserId!.Value);

        if (Application == null) return RedirectToPage("/Applications/Index");

        ViewData["AppId"] = appId;
        ViewData["ActiveTab"] = "home";
        ViewData["AppReference"] = Application.ReferenceNumber;
        ViewData["AppSubclassName"] = Application.Subclass!.Name;
        ViewData["Title"] = $"Application {Application.ReferenceNumber}";
        return Page();
    }
}
