using ImmiAccount.Data;
using ImmiAccount.Models;
using Microsoft.AspNetCore.Mvc;

namespace ImmiAccount.Pages;

public class ManageAccountModel : PageModelBase
{
    private readonly AppDbContext _db;

    public ManageAccountModel(AppDbContext db) => _db = db;

    public User? CurrentUser { get; set; }
    public bool SaveSuccess { get; set; }
    public string? SaveError { get; set; }

    public IActionResult OnGet()
    {
        var redirect = CheckAuth();
        if (redirect != null) return redirect;

        CurrentUser = _db.Users.Find(CurrentUserId!.Value);
        return Page();
    }

    public IActionResult OnPost(string displayName, string email, string? phone)
    {
        var redirect = CheckAuth();
        if (redirect != null) return redirect;

        if (string.IsNullOrWhiteSpace(displayName) || string.IsNullOrWhiteSpace(email))
        {
            SaveError = "An error has occurred. Please check your input and try again.";
            CurrentUser = _db.Users.Find(CurrentUserId!.Value);
            return Page();
        }

        var user = _db.Users.Find(CurrentUserId!.Value);
        if (user == null) return RedirectToPage("/Login");

        user.DisplayName = displayName.Trim();
        user.Email = email.Trim();
        user.Phone = phone?.Trim();
        _db.SaveChanges();

        HttpContext.Session.SetString("DisplayName", user.DisplayName);
        SaveSuccess = true;
        CurrentUser = user;
        return Page();
    }
}
