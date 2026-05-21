using ImmiAccount.Data;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace ImmiAccount.Pages;

public class LoginModel : PageModel
{
    private readonly AppDbContext _db;

    public LoginModel(AppDbContext db) => _db = db;

    public string? ErrorMessage { get; set; }
    public string? TimeoutMessage { get; set; }

    public void OnGet()
    {
        TimeoutMessage = TempData["TimeoutMessage"]?.ToString();
    }

    public IActionResult OnPost(string username, string password)
    {
        var user = _db.Users
            .FirstOrDefault(u => u.Username == username && u.Password == password);

        if (user == null)
        {
            ErrorMessage = "An error has occurred. Please check your username and password and try again.";
            return Page();
        }

        HttpContext.Session.SetInt32("UserId", user.Id);
        HttpContext.Session.SetString("DisplayName", user.DisplayName);
        HttpContext.Session.SetString("LastActivity", DateTime.UtcNow.ToString("O"));
        return RedirectToPage("/Applications/Index");
    }
}
